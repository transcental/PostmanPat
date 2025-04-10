import os

from aiohttp import ClientSession
from dotenv import load_dotenv
from slack_sdk.web.async_client import AsyncWebClient

from postmanpat.utils.airtable.manager import AirtableManager


load_dotenv(override=True)


class Environment:
    def __init__(self):
        self.slack_app_token = os.environ.get("SLACK_APP_TOKEN")
        self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN", "unset")
        self.slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "unset")
        self.slack_heartbeat_channel = os.environ.get("SLACK_HEARTBEAT_CHANNEL")

        self.airtable_api_key = os.environ.get("AIRTABLE_API_KEY", "unset")
        self.airtable_base_id = os.environ.get("AIRTABLE_BASE_ID", "unset")
        self.airtable_posties_table_id = os.environ.get(
            "AIRTABLE_POSTIES_TABLE_ID", "unset"
        )
        self.airtable_requests_table_id = os.environ.get(
            "AIRTABLE_REQUESTS_TABLE_ID", "unset"
        )

        self.environment = os.environ.get("ENVIRONMENT", "development")

        self.port = int(os.environ.get("PORT", 3000))

        unset = [key for key, value in self.__dict__.items() if value == "unset"]

        if unset:
            raise ValueError(f"Missing environment variables: {', '.join(unset)}")

        self.session: ClientSession

        self.slack_client = AsyncWebClient(token=self.slack_bot_token)
        self.airtable_client = AirtableManager(
            base_id=self.airtable_base_id,
            api_key=self.airtable_api_key,
            posties_table_name=self.airtable_posties_table_id,
            requests_table_name=self.airtable_requests_table_id,
        )


env = Environment()
