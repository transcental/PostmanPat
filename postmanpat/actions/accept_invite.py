import time

from slack_bolt.async_app import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from postmanpat.utils.env import env
from postmanpat.views.modals.manager.accept_invite import get_accept_invite_view


async def accept_invite_callback(ack: AsyncAck, body, client: AsyncWebClient):
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

    user = env.airtable_client.get_postie_by_slack_id(user_id)
    if user:
        return await client.chat_postMessage(
            text="hey silly, you can't accept an invite to a team you're already in!\n\ncheerio now pal, pat :)",
            channel=user_id,
        )

    message_ts = body["message"]["ts"]
    metadata = f"{inviter}-{action_id.split('-')[1]}-{message_ts}"
    view = get_accept_invite_view(user_id, metadata)
    await client.views_open(trigger_id=trigger_id, view=view)
