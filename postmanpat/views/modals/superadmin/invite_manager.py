from typing import Any


def get_invite_manager_view() -> dict[str, Any]:
    return {
        "type": "modal",
        "callback_id": "invite-manager",
        "title": {"type": "plain_text", "text": "Invite as Manager"},
        "submit": {"type": "plain_text", "text": "Invite"},
        "close": {"type": "plain_text", "text": "Cancel"},
        "blocks": [
            {
                "type": "input",
                "block_id": "user-select",
                "dispatch_action": True,
                "label": {
                    "type": "plain_text",
                    "text": "Choose a user to invite as a manager",
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
                    "action_id": "invite-manager",
                },
            }
        ],
    }
