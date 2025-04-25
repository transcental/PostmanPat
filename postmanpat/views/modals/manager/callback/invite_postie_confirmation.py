import logging
import time

from slack_bolt.async_app import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from postmanpat.utils.env import env
from postmanpat.utils.logging import send_heartbeat


async def check_user(ack: AsyncAck, body, client: AsyncWebClient):
    selected_user = body["view"]["state"]["values"]["user-select"]["invite-postie"][
        "selected_user"
    ]
    is_postie = env.airtable_client.get_postie_by_slack_id(selected_user)

    if is_postie:
        logging.info(f"User {selected_user} is already in the team")
        return await ack(
            response_action="errors",
            errors={"user-select": "User is already in the team!"},
        )
    return await ack()


async def invite_postie_confirmation_callback(
    ack: AsyncAck, body, client: AsyncWebClient
):
    await ack()
    selected_user = body["view"]["private_metadata"]
    user_id = body["user"]["id"]

    postie = env.airtable_client.get_postie_by_slack_id(user_id)
    if not postie or not postie.is_manager:
        await send_heartbeat(
            f"<@{user_id}> is not a manager and tried to invite <@{selected_user}>"
        )
        return await client.chat_postMessage(
            text="heya! You gotta be a manager to invite a postie :3",
            channel=user_id,
        )

    new_manager = env.airtable_client.get_postie_by_slack_id(selected_user)
    if new_manager:
        await send_heartbeat(
            f"<@{user_id}> attempted to invite <@{selected_user}> as a postie (they're already in the team!)"
        )

        return await client.chat_postMessage(
            text="heya! This user is already a postie, so i can't do anything here!\nsorry pal, i don't make the guides 'round here \n\ncheerio - pat :)",
            channel=user_id,
        )

    await send_heartbeat(
        f"<@{user_id}> is inviting <@{selected_user}> to mail team as a postie"
    )
    now = time.time()
    await client.chat_postMessage(
        channel=selected_user,
        text="heya! You've been invited to join the mail team as a *postie*! woah!\n\nplease check out the message below and accept or reject the invite!",
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"heya pal! <@{user_id}> has invited you to join the mail team as a *postie*! woah!\nit looks like you're new to the team though so i'm going to need you to give me a bit of info about ya.\nsorry, i know it's boring but we gotta get the paperwork in order\n\nhave a good one! pat :)\n\nps: you have one week to accept this invite!",
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "accept", "emoji": True},
                        "value": f"{user_id}-{now}",
                        "action_id": "accept-postie",
                        "style": "primary",
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "reject", "emoji": True},
                        "value": f"{user_id}-{now}",
                        "action_id": "reject-postie",
                        "style": "danger",
                    },
                ],
            },
        ],
    )
    return await client.chat_postMessage(
        text=f"how'd ya do? i've just sent an invite to <@{selected_user}> for mail team postie! i'll give them the quick rundown when they join but you should catch them up to speed yourself too! oh also, if they don't accept your invite in one week then you'll need to send them a new one\n\nanyway, cheerio! pat :)",
        channel=user_id,
    )
