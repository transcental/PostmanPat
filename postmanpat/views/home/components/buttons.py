from postmanpat.utils.airtable.types import Postie


def get_buttons(postie: Postie, current: str = "dashboard"):
    buttons = []

    buttons.append(
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "Dash", "emoji": True},
            "action_id": "dashboard",
            **({"style": "primary"} if current != "dashboard" else {}),
        }
    )

    if postie.fields.manager:
        buttons.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "Manage Posties", "emoji": True},
                "action_id": "manage-posties",
                **({"style": "primary"} if current != "manage-posties" else {}),
            }
        )
        buttons.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "Manage Mail", "emoji": True},
                "action_id": "manage-mail",
                **({"style": "primary"} if current != "manage-mail" else {}),
            }
        )
    if not postie.fields.on_hiatus:
        buttons.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "My Mail", "emoji": True},
                "action_id": "my-mail",
                **({"style": "primary"} if current != "my-mail" else {}),
            }
        )

    blocks = {"type": "actions", "elements": buttons}
    return blocks
