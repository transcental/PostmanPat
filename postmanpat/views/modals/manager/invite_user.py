from typing import Any
from typing import Literal


def get_invite_view(role: Literal["Manager", "Postie"]) -> dict[str, Any]:
    return {
        "type": "modal",
        "callback_id": f"invite-{role.lower()}",
        "title": {"type": "plain_text", "text": f"Invite as {role}"},
        "submit": {"type": "plain_text", "text": "Invite"},
        "close": {"type": "plain_text", "text": "Cancel"},
        "blocks": [
            {
                "type": "input",
                "block_id": "user-select",
                "dispatch_action": True,
                "label": {
                    "type": "plain_text",
                    "text": f"Choose a user to invite as a {role.lower()}",
                    "emoji": True,
                },
                "element": {
                    "type": "users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a user",
                        "emoji": True,
                    },
                    "focus_on_load": True,
                    "action_id": f"invite-{role.lower()}",
                },
            }
        ],
    }
