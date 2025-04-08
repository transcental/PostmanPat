from slack_bolt.async_app import AsyncApp
from slack_bolt.context.ack.async_ack import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from postmanpat.events.app_home_opened import on_app_home_opened
from postmanpat.events.app_home_opened import open_app_home
from postmanpat.utils.env import env

app = AsyncApp(token=env.slack_bot_token, signing_secret=env.slack_signing_secret)


@app.event("app_home_opened")
async def app_home_opened_handler(event, client: AsyncWebClient):
    await on_app_home_opened(event, client)


@app.action("dashboard")
@app.action("manage-posties")
@app.action("manage-mail")
@app.action("my-mail")
async def manage_view_switcher(ack: AsyncAck, body, client: AsyncWebClient):
    await ack()
    user_id = body["user"]["id"]
    action_id = body["actions"][0]["action_id"]

    await open_app_home(action_id, client, user_id)
