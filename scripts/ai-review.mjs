import { readFileSync } from "node:fs";

const githubToken = process.env.GITHUB_TOKEN;
const polzaApiKey = process.env.POLZA_AI_API_KEY;

const repository = process.env.GITHUB_REPOSITORY;
const pullNumber = process.env.PR_NUMBER;

const githubApiUrl = "https://api.github.com";
const polzaApiUrl = "https://polza.ai/api/v1/chat/completions";

const model = "anthropic/claude-sonnet-5";

if (!githubToken) {
  throw new Error("GITHUB_TOKEN is not set");
}

if (!polzaApiKey) {
  throw new Error("POLZA_AI_API_KEY is not set");
}

if (!repository || !pullNumber) {
  throw new Error("Repository or PR number is not set");
}


// ---------- GitHub ----------

async function githubRequest(path, options = {}) {
  const response = await fetch(`${githubApiUrl}${path}`, {
    ...options,
    headers: {
      Accept: "application/vnd.github+json",
      Authorization: `Bearer ${githubToken}`,
      "Content-Type": "application/json",
      "X-GitHub-Api-Version": "2022-11-28",
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(
      `GitHub API error ${response.status}: ${await response.text()}`
    );
  }

  return response.json();
}


// ---------- Get PR ----------

const pullRequest = await githubRequest(
  `/repos/${repository}/pulls/${pullNumber}`
);

console.log(`Reviewing PR #${pullNumber}: ${pullRequest.title}`);


// ---------- Get changed files ----------

const files = await githubRequest(
  `/repos/${repository}/pulls/${pullNumber}/files?per_page=100`
);

const changedFiles = files
  .filter((file) => file.status !== "removed")
  .map((file) => ({
    path: file.filename,
    patch: file.patch || "",
  }));

if (changedFiles.length === 0) {
  console.log("No changed files. Nothing to review.");
  process.exit(0);
}

const diff = changedFiles
  .map(
    (file) =>
      `FILE: ${file.path}\n${file.patch}`
  )
  .join("\n\n");


// ---------- Read review rules ----------

const rules = readFileSync(
  new URL("./ai-review-rules.md", import.meta.url),
  "utf8"
);


// ---------- Ask Claude ----------

const prompt = `
You are a code reviewer for a QA automation project.

Review the Pull Request according to the rules below.

IMPORTANT:
- Review only the code shown in the diff.
- Do not invent requirements.
- Do not complain about minor formatting or personal style preferences.
- Focus on real bugs, flaky tests, bad assertions, incorrect test logic,
  unnecessary duplication and maintainability problems.
- Only report problems that are actually supported by the rules.
- If there are no problems, return an empty comments array.

REVIEW RULES:

${rules}

PULL REQUEST:

Title:
${pullRequest.title}

Description:
${pullRequest.body || "(no description)"}

DIFF:

${diff}

Return JSON in exactly this format:

{
  "summary": "short overall review",
  "comments": [
    {
      "path": "path/to/file.py",
      "line": 10,
      "body": "Explain the problem and why it should be changed."
    }
  ]
}

The "line" must be a line that was ADDED in the diff.
`;


const response = await fetch(polzaApiUrl, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${polzaApiKey}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model,
    messages: [
      {
        role: "user",
        content: prompt,
      },
    ],
    max_completion_tokens: 3000,
  }),
});

if (!response.ok) {
  throw new Error(
    `Polza API error ${response.status}: ${await response.text()}`
  );
}

const data = await response.json();

const content = data.choices?.[0]?.message?.content;

if (!content) {
  throw new Error("Claude returned an empty response");
}


// ---------- Parse Claude response ----------

let review;

try {
  review = JSON.parse(content);
} catch {
  throw new Error(`Claude returned invalid JSON:\n${content}`);
}

console.log("AI summary:");
console.log(review.summary);

console.log(`Found ${review.comments.length} comments.`);


// ---------- Publish review ----------

const githubComments = review.comments
  .map((comment) => {
    const file = files.find(
      (file) => file.filename === comment.path
    );

    if (!file) {
      return null;
    }

    return {
      path: comment.path,
      line: comment.line,
      side: "RIGHT",
      body: comment.body,
    };
  })
  .filter(Boolean);


await githubRequest(
  `/repos/${repository}/pulls/${pullNumber}/reviews`,
  {
    method: "POST",
    body: JSON.stringify({
      commit_id: pullRequest.head.sha,
      body: `## 🤖 AI Review\n\n${review.summary}`,
      event: "COMMENT",
      comments: githubComments,
    }),
  }
);

console.log("AI review published successfully.");