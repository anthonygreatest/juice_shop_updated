from utils.schemas.send_feedback_request_schema import SendFeedbackGenRequestSchema


class SendComplaintRequestSchema(SendFeedbackGenRequestSchema):

    message: str

    model_config = {
        "populate_by_name": True
    }
