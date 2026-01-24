import allure


from utils.logger import get_logger

logger = get_logger('SCHEMA_ASSERTIONS')

@allure.step('Validating response schema')
def validate_response(schema, response):

    logger.info('Validating response schema')

    try:
        return schema.model_validate(response)
    except Exception:
        raise Exception('Wrong format')

    # validate(
    #     schema=schema,
    #     instance=response,
    #     format_checker=Draft202012Validator.FORMAT_CHECKER
    # )