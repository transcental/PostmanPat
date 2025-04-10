from postmanpat.utils.airtable.types import Postie
from postmanpat.views.home.components.buttons import get_buttons
from postmanpat.views.home.components.mail_pie import get_mail_pie_chart


async def get_manage_mail_view(postie: Postie):
    btns = get_buttons(postie, "manage-mail")

    pie_chart = await get_mail_pie_chart(postie)

    return {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "Manage Mail", "emoji": True},
            },
            btns,
            {
                "type": "divider",
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Send Mail",
                            "emoji": True,
                        },
                        "action_id": "admin-send-mail",
                        "style": "primary",
                    }
                ],
            },
            pie_chart,
            {
                "type": "divider",
            },
        ],
    }
