from datetime import datetime

from postmanpat.utils.airtable.types import Postie
from postmanpat.utils.airtable.types import ShippingReqStatus
from postmanpat.utils.env import env


async def get_user_card(postie: Postie, viewer: Postie):
    sentence = f"{':desert_island:' if not postie.is_working else ''} {':zap:' if postie.is_superadmin else ''} <@{postie.fields.slack_id}>"
    reqs = env.airtable_client.get_requests_by_postie_id(postie.fields.identifier)

    pending = 0
    shipped = 0

    for req in reqs:
        status = req.fields.status
        if status in [
            ShippingReqStatus.assigned,
            ShippingReqStatus.dispatched,
        ]:
            pending += 1
        elif status in [ShippingReqStatus.mailed, ShippingReqStatus.arrived]:
            shipped += 1
    sentence += f"\n*{pending}* items pending\n*{shipped}* items shipped"

    slack_user = await env.slack_client.users_info(user=postie.fields.slack_id)
    name = (
        slack_user.get("user", {}).get("profile", {}).get("real_name")
        or slack_user.get("user", {}).get("profile", {}).get("display_name")
        or "Postie"
    )
    pfp = (
        slack_user.get("user", {})
        .get("profile", {})
        .get(
            "image_512",
            "https://ca.slack-edge.com/T0266FRGM-U07MH63NPA6-88580da987bc-512",
        )
    )

    inviter = (
        f"<@{postie.inviter.fields.slack_id}>" if postie.inviter else "a mystical force"
    )
    date = datetime.fromisoformat(postie.fields.created_at)
    unix = int(date.timestamp())
    timestr = f"<!date^{unix}^{{ago}}|{date.strftime('%d %b %Y')}>"

    options = []

    if (viewer.is_manager and not postie.is_superadmin) or (viewer.id == postie.id):
        # Managers can update posties and managers (not superadmins)
        # Users can also update themselves
        options.append(
            {
                "text": {
                    "type": "plain_text",
                    "text": f"Update {name}",
                    "emoji": True,
                },
                "value": f"admin-update-{postie.id}",
            }
        )

    if viewer.is_superadmin and postie.is_regular_manager:
        # Superadmins can demote regular managers
        options.append(
            {
                "text": {
                    "type": "plain_text",
                    "text": f":zap: Demote {name}",
                    "emoji": True,
                },
                "value": f"superadmin-demote-{postie.id}",
            }
        )

    if viewer.is_superadmin and not postie.is_manager:
        # Superadmins can promote posties to managers
        options.append(
            {
                "text": {
                    "type": "plain_text",
                    "text": f":zap: Promote {name}",
                    "emoji": True,
                },
                "value": f"superadmin-promote-{postie.id}",
            }
        )

    if viewer.is_manager and not postie.is_manager:
        # Managers can kick regular posties
        options.append(
            {
                "text": {
                    "type": "plain_text",
                    "text": f"Remove {name}",
                    "emoji": True,
                },
                "value": f"admin-kick-{postie.id}",
            }
        )

    if viewer.is_superadmin and postie.is_regular_manager:
        # Superadmins can kick regular managers
        options.append(
            {
                "text": {
                    "type": "plain_text",
                    "text": f":zap: Remove {name}",
                    "emoji": True,
                },
                "value": f"superadmin-kick-{postie.id}",
            }
        )

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": sentence,
            },
            "accessory": {
                "type": "image",
                "image_url": pfp,
                "alt_text": f"{name}'s profile picture",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"_Joined {timestr}, invited by {inviter}_",
            },
            "accessory": {
                "type": "overflow",
                "options": options,
                "action_id": f"{viewer.fields.role}-update-user",
            },
        },
    ]
    return blocks
