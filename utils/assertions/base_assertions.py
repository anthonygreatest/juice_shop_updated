import allure

from utils.clients.event_hooks import get_logger

logger = get_logger("BASE_ASSERTIONS")

@allure.step('Check that response status code matches {expected}')
def assert_status_code(response, expected):

    logger.info(f'Check that response status code matches {expected}')

    assert response.status_code == expected, \
        f'Wrong status code, expected {expected}, got {response.status_code}'

@allure.step('Check that response status code matches one of {expected}')
def assert_status_code_among_expected(response, expected):

    logger.info(f'Check that response status code among {expected}')

    assert response.status_code in expected, \
        f'Wrong status code, expected {expected}, got {response.status_code}'

@allure.step('Check that {name} equals {expected}')
def assert_match(value, expected, name):

    logger.info(f'Check that {name} equals {expected}')

    assert value == expected, \
        f'Wrong {name}, expected {expected}, got {value}'


