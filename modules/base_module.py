

class BaseModule:

    def create_json_request(self, data, schema):
        return schema(**data).model_dump_json(by_alias=True)

    def create_request(self, data, schema):
        return schema(**data).model_dump(by_alias=True, mode='json')




