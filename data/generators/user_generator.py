import random
from datetime import datetime, timezone

from faker import Faker


from data.constants import SECURITY_QUESTIONS, WORKS_OF_ART


def user_generator():
    faker = Faker()
    question_id = random.randint(1, len(SECURITY_QUESTIONS) - 1)
    question = SECURITY_QUESTIONS[question_id]
    my_time = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

    if 'first name' in question or 'middle name' in question or 'pet' in question:
        if 'Mother' in question:
            security_answer = faker.name_female()
        elif 'Father' in question:
            security_answer = faker.name_male()
        else:
            security_answer = faker.first_name()
    elif 'Last name' in question or 'maiden name' in question:
        security_answer = faker.last_name()
    elif 'Number' in question or 'code' in question:
        security_answer = str(faker.random_number(fix_len=True, digits=8))
    elif 'date' in question:
        security_answer = faker.date_of_birth(minimum_age=30).strftime('%m/%d/%Y')
    elif 'movie' in question or 'book' in question:
        random_book_or_movie = random.choice(WORKS_OF_ART)
        security_answer = random_book_or_movie.strip()
    elif 'Company' in question:
        security_answer = faker.company()
    elif 'place' in question:
        security_answer = faker.city()

    return {
        'email': None,
        'password': None,
        'password_repeat': None,
        'security_question': {
            'id': question_id,
            'question': question,
            'created_at': my_time,
            'updated_at': my_time
        },
        'security_answer': security_answer

    }
