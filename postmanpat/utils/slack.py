import time

from slack_bolt.async_app import AsyncApp
from slack_bolt.context.ack.async_ack import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from postmanpat.actions.open_view import open_view
from postmanpat.events.app_home_opened import on_app_home_opened
from postmanpat.events.app_home_opened import open_app_home
from postmanpat.options.country import country_options
from postmanpat.options.currency import currency_options
from postmanpat.utils.env import env
from postmanpat.views.modals.manager.accept_invite import get_accept_invite_view
from postmanpat.views.modals.manager.callback.accept_invite import (
    accept_invite_callback,
)
from postmanpat.views.modals.superadmin.callback.invite_manager import check_user
from postmanpat.views.modals.superadmin.callback.invite_manager import (
    invite_manager_callback,
)
from postmanpat.views.modals.superadmin.callback.invite_manager_confirmation import (
    invite_manager_confirmation_callback,
)

app = AsyncApp(token=env.slack_bot_token, signing_secret=env.slack_signing_secret)


@app.event("app_home_opened")
async def app_home_opened_handler(event, client: AsyncWebClient):
    await on_app_home_opened(event, client)


@app.action("dashboard")
@app.action("manage-posties")
@app.action("manage-mail")
@app.action("my-mail")
async def manage_home_switcher(ack: AsyncAck, body, client: AsyncWebClient):
    await ack()
    user_id = body["user"]["id"]
    action_id = body["actions"][0]["action_id"]

    await open_app_home(action_id, client, user_id)


@app.action("superadmin-invite-manager")
async def manage_modal_opener(ack: AsyncAck, body, client: AsyncWebClient):
    await ack()
    user_id = body["user"]["id"]
    action_id = body["actions"][0]["action_id"]
    trigger_id = body["trigger_id"]
    await open_view(action_id, client, user_id, trigger_id)


@app.action("invite-manager")
async def invite_manager_action(ack: AsyncAck, body, client: AsyncWebClient):
    await check_user(ack, body, client)


@app.view("invite-manager")
async def invite_manager(ack: AsyncAck, body, client: AsyncWebClient):
    await invite_manager_callback(ack, body, client)


@app.view("invite-manager-confirmation")
async def invite_manager_confirmation(ack: AsyncAck, body, client: AsyncWebClient):
    await ack()
    await invite_manager_confirmation_callback(ack, body, client)


@app.options("country")
async def country_select(payload: dict, ack: AsyncAck):
    await country_options(ack, payload)


@app.options("currency")
async def currency_select(payload: dict, ack: AsyncAck):
    await currency_options(ack, payload)


@app.action("accept-manager")
async def accept_invite(ack: AsyncAck, body, client: AsyncWebClient):
    await ack()
    user_id = body["user"]["id"]
    action_id = body["actions"][0]["action_id"]
    trigger_id = body["trigger_id"]
    value = body["actions"][0]["value"]
    inviter = value.split("-")[0]
    sent = value.split("-")[1]
    now = int(time.time())
    if now - int(float(sent)) > 604800:
        return await client.chat_postMessage(
            text="heya!\nsorry mate, but this invite has expired! please ask your manager to send you a new one!\n\ncheerio - pat :)",
            channel=user_id,
        )

    metadata = f"{inviter}-{action_id.split('-')[1]}"
    view = get_accept_invite_view(user_id, metadata)
    await client.views_open(trigger_id=trigger_id, view=view)


@app.view("accept-invite")
async def complete_invite_form(ack: AsyncAck, body, client: AsyncWebClient):
    await accept_invite_callback(ack, body, client)
