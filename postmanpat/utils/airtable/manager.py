from pyairtable import Api

from postmanpat.utils.airtable.types import Postie
from postmanpat.utils.airtable.types import ShippingRequest


class AirtableManager:
    def __init__(
        self,
        base_id: str,
        api_key: str,
        posties_table_name: str,
        requests_table_name: str,
    ):
        self.airtable = Api(api_key)
        self.posties_table = self.airtable.table(base_id, posties_table_name)
        self.requests_table = self.airtable.table(base_id, requests_table_name)

    def get_posties(
        self,
        view: str = "Everyone",
        fields: list | None = None,
        formula: str | None = None,
    ):
        posties = self.posties_table.all(view=view, fields=fields, formula=formula)
        return posties

    def get_requests(
        self,
        view: str = "Everything",
        fields: list | None = None,
        formula: str | None = None,
    ) -> list[ShippingRequest] | None:
        requests = self.requests_table.all(view=view, fields=fields, formula=formula)
        if requests:
            requests = [ShippingRequest.parse_obj(req) for req in requests]
        else:
            requests = None
        return requests

    def get_postie(self, postie_id: str, fields: list | None = None):
        postie = self.posties_table.get(postie_id, fields=fields)
        return postie

    def get_postie_by_slack_id(
        self, slack_id: str, fields: list | None = None
    ) -> Postie | None:
        postie = self.posties_table.first(
            formula=f"{{slack_id}} = '{slack_id}'", fields=fields
        )
        if postie:
            postie = Postie.parse_obj(postie)
        return postie

    def get_request(self, request_id: str, fields: list | None = None):
        request = self.requests_table.get(request_id, fields=fields)
        return request
