import logging

from slack_bolt.async_app import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from postmanpat.utils.env import env
from postmanpat.views.modals.superadmin.invite_manager_confirmation import (
    get_invite_manager_confirmation_view,
)


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


async def invite_manager_callback(ack: AsyncAck, body, client: AsyncWebClient):
    view = body.get("view")
    selected_user = view["state"]["values"]["user-select"]["invite-manager"][
        "selected_user"
    ]

    is_postie = env.airtable_client.get_postie_by_slack_id(selected_user)
    if is_postie:
        logging.info(f"User {selected_user} is already in the team")
        return await ack(
            response_action="errors",
            errors={"user-select": "User is already in the team!"},
        )

    view = get_invite_manager_confirmation_view(selected_user)

    await ack(response_action="update", view=view)
