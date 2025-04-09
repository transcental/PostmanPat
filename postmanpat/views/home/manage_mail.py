import io
import logging

import matplotlib.pyplot as plt
import numpy as np

from postmanpat.utils.airtable.types import Postie
from postmanpat.utils.airtable.types import ShippingReqStatus
from postmanpat.utils.env import env
from postmanpat.views.home.components.buttons import get_buttons


async def get_manage_mail_view(postie: Postie):
    btns = get_buttons(postie, "manage-mail")

    all_mail = env.airtable_client.get_requests()

    status_counts = {
        ShippingReqStatus.pending: 0,
        ShippingReqStatus.assigned: 0,
        ShippingReqStatus.dispatched: 0,
        ShippingReqStatus.mailed: 0,
        ShippingReqStatus.arrived: 0,
        ShippingReqStatus.errored: 0,
        ShippingReqStatus.draft: 0,
    }

    for mail in all_mail:
        status_counts[mail.fields.status] += 1

    y = [count for count in status_counts.values()]
    labels = [
        "Unassigned",
        "Assigned",
        "Dispatched",
        "Mailed",
        "Arrived",
        "Errored",
        "Draft",
    ]
    colours = [
        "#C8C4E0",
        "#F4D3F9",
        "#FBEBBC",
        "#CCF3F0",
        "#D6F4D4",
        "#F4B994",
        "#CFD2D8",
    ]

    for count in range(
        len(y) - 1, -1, -1
    ):  # iterate in reverse so that indexes are not affected
        if y[count] == 0:
            del y[count]
            del labels[count]
            del colours[count]

    y = np.array(y)

    plt.pie(y, labels=labels, colors=colours, autopct="%1.1f%%", startangle=140)

    b = io.BytesIO()
    plt.savefig(
        b, bbox_inches="tight", pad_inches=0.1, transparent=True, dpi=300, format="png"
    )
    plt.close()

    res = await env.slack_client.files_upload_v2(
        content=b.getvalue(),
        filename="pie_chart.png",
        title="Mail stats",
        channel="C08MZU74HNC",
    )

    logging.info(res)
    file = res["file"]["id"]

    return {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "Manage Mail", "emoji": True},
            },
            btns,
            {"type": "divider"},
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "Manage Mail", "emoji": True},
            },
            {
                "type": "divider",
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*This is still a work in progress*",
                },
                "accessory": {
                    "type": "image",
                    "slack_file": {
                        "id": file,
                    },
                    "alt_text": "Pie Chart",
                },
            },
            {
                "type": "divider",
            },
        ],
    }
