from postmanpat.utils.airtable.types import Postie
from postmanpat.utils.env import env
from postmanpat.views.home.components.buttons import get_buttons
from postmanpat.views.home.components.user_card import get_user_card


async def get_manage_posties_view(postie: Postie):
    all_posties = env.airtable_client.get_posties()

    managers = [postie for postie in all_posties if postie.is_manager]
    posties = [postie for postie in all_posties if not postie.is_manager]

    manager_blocks = [
        await get_user_card(postie=manager, viewer=postie) for manager in managers
    ]
    postie_blocks = [
        await get_user_card(postie=person, viewer=postie) for person in posties
    ]

    btns = get_buttons(postie, "manage-posties")

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "Manage Posties", "emoji": True},
        },
        btns,
        {"type": "divider"},
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "Managers", "emoji": True},
        },
    ]
    blocks.extend(*manager_blocks)

    if postie.is_superadmin:
        blocks.append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": ":zap: Invite Manager",
                            "emoji": True,
                        },
                        "action_id": "superadmin-invite-manager",
                        "style": "primary",
                    }
                ],
            }
        )

    blocks.extend(
        [
            {"type": "divider"},
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "Posties", "emoji": True},
            },
        ]
    )

    blocks.extend(*postie_blocks)

    if postie.is_manager:
        blocks.append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Invite Postie",
                            "emoji": True,
                        },
                        "action_id": "admin-invite-postie",
                        "style": "primary",
                    }
                ],
            }
        )

    return {"type": "home", "blocks": blocks}
