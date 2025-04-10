from io import BytesIO

import numpy as np

from postmanpat.utils.airtable.types import Postie
from postmanpat.utils.airtable.types import ShippingReqStatus
from postmanpat.utils.env import env
from postmanpat.utils.graphs.pie import generate_pie_chart
from postmanpat.utils.time.is_day import is_day
from postmanpat.utils.upload.litterbox import upload_litter


async def get_mail_pie_chart(postie: Postie):
    is_daytime = is_day(
        city=postie.fields.city,
    )

    if is_daytime:
        text_colour = "black"
        bg_colour = "white"
    else:
        text_colour = "white"
        bg_colour = "#181A1E"

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

    b = BytesIO()
    plt = generate_pie_chart(
        y=y,
        labels=labels,
        colours=colours,
        text_colour=text_colour,
        bg_colour=bg_colour,
    )
    plt.savefig(
        b, bbox_inches="tight", pad_inches=0.1, transparent=False, dpi=300, format="png"
    )

    url = await upload_litter(
        file=b.getvalue(),
        filename="mail_stats.png",
        expiry="1h",
        content_type="image/png",
    )
    caption = "Mail stats"

    if not url:
        url = "https://hc-cdn.hel1.your-objectstorage.com/s/v3/0cd2e596df17b801ca2eabeab0130f3d08143e4e_postman-pat-collecting.gif"
        caption = "Looks like Pat's still sorting mail"

    return {
        "type": "image",
        "title": {
            "type": "plain_text",
            "text": caption,
            "emoji": True,
        },
        "image_url": url,
        "alt_text": "Mail stats",
    }
