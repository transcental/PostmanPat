from slack_bolt.async_app import AsyncApp

from postmanpat.events.app_home_opened import on_app_home_opened
from postmanpat.utils.env import env

app = AsyncApp(token=env.slack_bot_token, signing_secret=env.slack_signing_secret)


@app.event("app_home_opened")
async def app_home_opened_handler(event, client):
    await on_app_home_opened(event, client)
