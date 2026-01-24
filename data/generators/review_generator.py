import random

from data.dataclasses.feedback_data import FeedbackData
from data.generators.generator import BaseFakerGenerator


class ReviewGenerator(BaseFakerGenerator):

    def generate_review(self):

        review = self.faker.sentence()

        return review

class FeedbackGenerator(BaseFakerGenerator):

    def generate_feedback(self):
        comment = ReviewGenerator().generate_review()
        rating = random.randint(1, 5)

        return FeedbackData(
            comment=comment,
            rating=rating
        )
