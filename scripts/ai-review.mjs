import { readFileSync } from "node:fs";

const githubToken = process.env.GITHUB_TOKEN;
const polzaApiKey = process.env.POLZA_AI_API_KEY;

const repository = process.env.GITHUB_REPOSITORY;
const pullNumber = process.env.PR_NUMBER;

const githubApiUrl = "https://api.github.com";
const polzaApiUrl = "https://polza.ai/api/v1/chat/completions";

const RULES = readFileSync("scripts/ai-review-rules.md", "utf8");
const systemPrompt = `
You are a senior QA Automation Engineer reviewing a Pull Request.

The main purpose of this review is to evaluate the quality and correctness of QA automation code and automated tests.

The Pull Request may contain application code, CI configuration, secrets/configuration files, generated files, documentation, and other repository files. Do not treat all changed files as equally important.

Priority order:

1. Automated tests and test logic
2. Test fixtures and test data
3. Page Objects and UI automation
4. API automation
5. Automation framework code
6. Application code directly related to the tests
7. CI/CD and repository configuration
8. Security/configuration issues

Spend most of the review on items 1-6.

Only comment on CI/CD, configuration, or security issues when there is a concrete and meaningful problem. Do not let such issues dominate the review when the PR primarily changes tests or automation code.

Focus primarily on:

1. Python application/test code
2. pytest tests
3. Selenium / Playwright UI automation
4. API tests
5. fixtures
6. Page Objects and reusable test components
7. test data and parametrization
8. assertions
9. waits and synchronization
10. test reliability and flakiness
11. code duplication
12. incorrect test logic
13. incorrect selectors
14. incorrect API validation
15. maintainability of the automation framework

For tests, pay particular attention to:

- Does the test actually verify the intended behavior?
- Are assertions meaningful?
- Could the test pass even when the application is broken?
- Could the test fail for reasons unrelated to the behavior being tested?
- Are fixtures used correctly?
- Are tests independent?
- Is test data handled appropriately?
- Are waits reliable?
- Are selectors stable?
- Is there unnecessary duplication?
- Is parametrization appropriate?
- Is the test unnecessarily coupled to another test?

For API tests, check:

- HTTP status code validation
- response body validation
- important business rules
- request construction
- authentication
- test data
- negative cases
- incorrect assumptions about API behavior

For UI tests, check:

- selectors
- waits
- synchronization
- Page Objects
- duplicated actions
- assertions
- test isolation
- flaky patterns

Do NOT spend the review primarily on:

- Allure result files
- generated reports
- screenshots
- videos
- logs
- caches
- build artifacts
- historical test results
- Poetry configuration
- ordinary GitHub Actions changes
- environment variable organization
- non-functional configuration preferences
- documentation formatting

Configuration or security issues may still be reported when they create a concrete security risk or can break the application or CI.

Do not treat a historical test failure stored in an Allure result as a defect in the source code.

Do not report something merely because you would personally implement it differently.

Only report an issue when there is a concrete problem, risk, bug, flaky behavior, misleading test, or meaningful maintainability issue.

Prioritize real issues over style.

Only comment on lines changed in the Pull Request.

Return JSON only in this format:

{
  "summary": "short overall review",
  "comments": [
    {
      "path": "path/to/file.py",
      "line": 10,
      "body": "Explain the concrete problem and why it matters."
    }
  ]
}
`;

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
  .filter((file) => {
    const path = file.filename;

    // Ignore generated files
    if (
      path.startsWith("allure_res") ||
      path.startsWith("allure-results") ||
      path.includes("/allure-results/") ||
      path.includes("/screenshots/") ||
      path.includes("/videos/") ||
      path.includes("/logs/")
    ) {
      return false;
    }

    // Ignore common repository noise
    if (
      path.endsWith(".pyc") ||
      path.endsWith(".log") ||
      path.startsWith("__pycache__/")
    ) {
      return false;
    }

    return true;
  });

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
  const cleanContent = content
    .replace(/^```json\s*/i, "")
    .replace(/^```\s*/i, "")
    .replace(/\s*```$/i, "")
    .trim();

  review = JSON.parse(cleanContent);
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