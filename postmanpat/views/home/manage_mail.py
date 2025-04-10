from postmanpat.utils.airtable.types import Postie
from postmanpat.utils.env import env
from postmanpat.views.home.components.buttons import get_buttons
from postmanpat.views.home.components.countries_bar_chart import get_countries_bar_chart
from postmanpat.views.home.components.mail_pie import get_mail_pie_chart


async def get_manage_mail_view(postie: Postie):
    btns = get_buttons(postie, "manage-mail")

    all_mail = env.airtable_client.get_requests()
    pie_chart = await get_mail_pie_chart(postie, all_mail)
    stacked_bar_chart = await get_countries_bar_chart(postie, all_mail)

    sent_mail = [mail for mail in all_mail if mail.is_sent]
    postie_ids = set([mail.postie for mail in sent_mail if mail.postie])

    sent_mail_by_postie = {
        postie_id: [mail for mail in sent_mail if mail.postie == postie_id]
        for postie_id in postie_ids
    }
    sent_mail_by_postie = sorted(
        sent_mail_by_postie.items(), key=lambda x: len(x[1]), reverse=True
    )
    arrived_mail_by_postie = {
        postie_id: [
            mail for mail in sent_mail if mail.postie == postie_id and mail.has_arrived
        ]
        for postie_id in postie_ids
    }
    posties = env.airtable_client.get_posties_by_ids(list(postie_ids))

    sent_mail_by_postie_blocks = []

    for postie_id, mails in sent_mail_by_postie:
        ps = next((p for p in posties if p.id == postie_id), None)
        total_arrived = len(arrived_mail_by_postie.get(postie_id, []))
        if ps:
            sent_mail_by_postie_blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*<@{ps.fields.slack_id}>*: {len(mails)} sent ({total_arrived} arrived)",
                    },
                }
            )

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
            stacked_bar_chart,
            {
                "type": "divider",
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Sent Mail by Postie",
                    "emoji": True,
                },
            },
            *sent_mail_by_postie_blocks,
        ],
    }
