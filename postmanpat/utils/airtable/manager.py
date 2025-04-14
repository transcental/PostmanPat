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

    def get_posties_by_ids(self, postie_ids: list[str], fields: list | None = None):
        formula = (
            "OR("
            + ",".join([f"RECORD_ID()='{postie_id}'" for postie_id in postie_ids])
            + ")"
        )

        posties = self.posties_table.all(formula=formula, fields=fields)

        if posties:
            posties = [Postie.parse_obj(postie) for postie in posties]
        else:
            posties = []
        return posties

    def get_posties(
        self,
        view: str = "Everyone",
        fields: list | None = None,
        formula: str | None = None,
    ) -> list[Postie]:
        posties = self.posties_table.all(view=view, fields=fields, formula=formula)
        return [Postie.parse_obj(postie) for postie in posties] if posties else []

    def get_requests(
        self,
        view: str = "Everything",
        fields: list | None = None,
        formula: str | None = None,
    ) -> list[ShippingRequest]:
        requests = self.requests_table.all(view=view, fields=fields, formula=formula)
        if requests:
            requests = [ShippingRequest.parse_obj(req) for req in requests]
        else:
            requests = []
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

    def update_postie_by_id(self, postie_id: str, fields: dict):
        postie = self.posties_table.update(postie_id, fields=fields)
        if postie:
            postie = Postie.parse_obj(postie)
        return postie

    def create_postie(self, fields: dict):
        postie = self.posties_table.create(fields)
        if postie:
            postie = Postie.parse_obj(postie)
        return postie

    def get_request(self, request_id: str, fields: list | None = None):
        request = self.requests_table.get(request_id, fields=fields)
        return request

    def get_requests_by_postie_id(
        self, postie_id: str, fields: list | None = None
    ) -> list[ShippingRequest]:
        requests = self.requests_table.all(
            formula=f"{{postie}} = '{postie_id}'", fields=fields
        )

        if requests:
            requests = [ShippingRequest.parse_obj(req) for req in requests]
        else:
            requests = []
        return requests
