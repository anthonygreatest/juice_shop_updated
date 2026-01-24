import json

from utils.clients.api_client import BaseClient


class RawAPIClient(BaseClient):


    def _resolve_endpoint(self, endpoint):
        if isinstance(endpoint, str):
            return getattr(self.endpoints, endpoint)
        return endpoint


    def get(self, endpoint, params=None, headers=None):
        url = self._resolve_endpoint(endpoint=endpoint)
        return super().get(
            url=url,
            params=params,
            headers=headers
        )

    def post(self, endpoint, data, headers=None):
        url = self._resolve_endpoint(endpoint=endpoint)
        return super().post(
            url=url,
            json=data,
            headers=headers
        )

    def put(self, endpoint, data, headers=None):
        url = self._resolve_endpoint(endpoint=endpoint)
        return super().put(
            url=url,
            json=data,
            headers=headers
        )

    def delete(self, endpoint, headers=None):
        url = self._resolve_endpoint(endpoint=endpoint)
        return super().delete(
            url=url,
            headers=headers
        )

    def put_with_id(self, data, endpoint_id, endpoint, headers=None):
        url = self._resolve_endpoint(endpoint=endpoint)
        final_url = f'{url}/{endpoint_id}'
        return super().put(
            url=final_url,
            json=data,
            headers=headers
        )

    def post_with_id(self, data, endpoint_id, endpoint, headers=None):
        url = self._resolve_endpoint(endpoint=endpoint)
        final_url = f'{url}/{endpoint_id}'
        return super().post(
            url=final_url,
            json=data,
            headers=headers
        )

    def get_with_id(self, params, endpoint_id, endpoint, headers=None):
        url = self._resolve_endpoint(endpoint=endpoint)
        final_url = f'{url}/{endpoint_id}'
        return super().get(
            url=final_url,
            params=params,
            headers=headers
        )

    def finalize_order_at_checkout(self, data, endpoint, basket_id, headers=None):
        url = self._resolve_endpoint(endpoint=endpoint)
        final_url = url(basket_id)
        return super().post(
            url=final_url,
            json=data,
            headers=headers
        )

    def leave_review(self, data, endpoint, product_id, headers=None):
        url = self._resolve_endpoint(endpoint=endpoint)
        final_url = url(product_id)
        return super().put(
            url=final_url,
            json=data,
            headers=headers
        )

    def leave_review_invalid_method(self, data, endpoint_id, endpoint, headers=None):
        url = self._resolve_endpoint(endpoint=endpoint)
        final_url = url(endpoint_id)
        return super().post(
            url=final_url,
            json=data,
            headers=headers
        )

    def post_with_raw_headers(self, endpoint, data, headers):
        url = self._resolve_endpoint(endpoint=endpoint)
        return super().post(
            url=url,
            data=json.dumps(data),
            headers=headers
        )

    def post_with_id_with_raw_headers(self, endpoint_id, endpoint, data, headers):
        url = self._resolve_endpoint(endpoint=endpoint)
        final_url = url(endpoint_id)
        return super().post(
            url=final_url,
            data=json.dumps(data),
            headers=headers
        )

    def put_with_id_with_raw_headers(self, endpoint_id, endpoint, data, headers):
        url = self._resolve_endpoint(endpoint=endpoint)
        final_url = url(endpoint_id)
        return super().put(
            url=final_url,
            data=json.dumps(data),
            headers=headers
        )
