from typing import Any


def get_invite_manager_confirmation_view(user_id: str) -> dict[str, Any]:
    return {
        "type": "modal",
        "callback_id": "invite-manager-confirmation",
        "title": {"type": "plain_text", "text": "Invite as Manager"},
        "submit": {"type": "plain_text", "text": "Invite"},
        "close": {"type": "plain_text", "text": "Back"},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Are you sure you want to invite <@{user_id}> as a manager?",
                },
            },
            {
                "type": "rich_text",
                "block_id": "3MQ8Y",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": "Managers can do the following:",
                                "style": {"bold": True},
                            },
                            {"type": "text", "text": "\n"},
                        ],
                    },
                    {
                        "type": "rich_text_list",
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "Add",
                                        "style": {"bold": True},
                                    },
                                    {"type": "text", "text": " and "},
                                    {
                                        "type": "text",
                                        "text": "remove",
                                        "style": {"bold": True},
                                    },
                                    {"type": "text", "text": " posties"},
                                ],
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "Update",
                                        "style": {"bold": True},
                                    },
                                    {"type": "text", "text": " and "},
                                    {
                                        "type": "text",
                                        "text": "view",
                                        "style": {"bold": True},
                                    },
                                    {"type": "text", "text": " postie information"},
                                ],
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "Order",
                                        "style": {"bold": True},
                                    },
                                    {
                                        "type": "text",
                                        "text": " packages to be sent to Hack Clubbers",
                                    },
                                ],
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "View",
                                        "style": {"bold": True},
                                    },
                                    {
                                        "type": "text",
                                        "text": " information for any sent packages",
                                    },
                                ],
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "Update",
                                        "style": {"bold": True},
                                    },
                                    {
                                        "type": "text",
                                        "text": " information for any pending packages",
                                    },
                                ],
                            },
                        ],
                        "style": "bullet",
                        "indent": 0,
                        "border": 0,
                    },
                ],
            },
        ],
        "private_metadata": user_id,
    }
