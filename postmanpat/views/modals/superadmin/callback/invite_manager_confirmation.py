import logging
import time

from slack_bolt.async_app import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from postmanpat.utils.env import env
from postmanpat.utils.logging import send_heartbeat


async def check_user(ack: AsyncAck, body, client: AsyncWebClient):
    selected_user = body["view"]["state"]["values"]["user-select"]["invite-manager"][
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


async def invite_manager_confirmation_callback(
    ack: AsyncAck, body, client: AsyncWebClient
):
    await ack()
    selected_user = body["view"]["private_metadata"]
    user_id = body["user"]["id"]

    postie = env.airtable_client.get_postie_by_slack_id(user_id)
    if not postie or not postie.is_superadmin:
        await send_heartbeat(
            f"<@{user_id}> is not a superadmin and tried to invite <@{selected_user}> as a manager"
        )
        return await client.chat_postMessage(
            text="heya! You gotta be a superadmin to invite a manager :3",
            channel=user_id,
        )

    new_manager = env.airtable_client.get_postie_by_slack_id(selected_user)
    if new_manager:
        await send_heartbeat(
            f"<@{user_id}> is promoting <@{selected_user}> to a manager"
        )
        env.airtable_client.update_postie_by_id(new_manager.id, {"role": "manager"})
        await client.chat_postMessage(
            text=f"heya buddy! <@{user_id}> has just promoted you to a *manager* on the mail team, woah!\nyou can now manage other posties including adding/removing them and updating their data! you also get to see a bunch of fancy stats on my app home!\n\ncheerio - pat",
            channel=selected_user,
        )

        return await client.chat_postMessage(
            text="heya! This user is already a postie, you should use the overflow menu to promote them instead! since you already went through this flow though i guess i'll do it for ya!\n\nhave a good one! pat :)",
            channel=user_id,
        )

    await send_heartbeat(
        f"<@{user_id}> is inviting <@{selected_user}> to mail team as a manager"
    )
    now = time.time()
    await client.chat_postMessage(
        channel=selected_user,
        text="heya! You've been invited to join the mail team as a *manager*! woah!\n\nplease check out the message below and accept the invite!",
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"heya pal! <@{user_id}> has invited you to join the mail team as a *manager*! woah!\nit looks like you're new to the team though so i'm going to need you to give me a bit of info about ya. dw about it too much unless you're planning on sending mail, it's easier to have a consistent system than make a separate system for managers my bosses tell me.\n\nhave a good one! pat :)\n\nps: you have one week to accept this invite!",
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "accept", "emoji": True},
                        "value": f"{user_id}-{now}",
                        "action_id": "accept-manager",
                        "style": "primary",
                    },
                ],
            },
        ],
    )
    return await client.chat_postMessage(
        text=f"how'd ya do? i've just sent an invite to <@{selected_user}> for mail team manager! i'll give them the quick rundown when they join but you should catch them up to speed yourself too! oh also, if they don't accept your invite in one week then you'll need to send them a new one\n\nanyway, cheerio! pat :)",
        channel=user_id,
    )
