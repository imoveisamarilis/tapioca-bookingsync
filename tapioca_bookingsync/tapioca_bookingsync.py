from tapioca import (TapiocaAdapter, generate_wrapper_from_adapter,
                     JSONAdapterMixin)
from requests_oauthlib import OAuth2
from .resource_mapping import RESOURCE_MAPPING


class BookingSyncClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'https://www.bookingsync.com/api/v3/'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(BookingSyncClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs
        )
        params['auth'] = OAuth2(
            api_params.get('client_id', ''),
            token={
                'access_token': api_params.get('access_token'),
                'token_type': 'Bearer'
            }
        )
        return params

    def get_iterator_list(self, response_data):
        return response_data

    def response_to_native(self, response):
        native = super(BookingSyncClientAdapter, self).response_to_native(
            response
        )
        items = []
        if native is None:
            return items

        assert isinstance(native, dict)
        for k, v in native.items():
            if isinstance(v, list):
                items.extend(v)
        return items

    def get_iterator_next_request_kwargs(self,
                                         iterator_request_kwargs,
                                         response_data,
                                         response):
        next_link = response.links.get('next')
        if next_link and 'url' in next_link.keys():
            return {'url': next_link['url']}


BookingSync = generate_wrapper_from_adapter(BookingSyncClientAdapter)
