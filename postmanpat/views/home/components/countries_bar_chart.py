from io import BytesIO

import numpy as np

from postmanpat.utils.airtable.types import Postie
from postmanpat.utils.airtable.types import ShippingReqStatus
from postmanpat.utils.airtable.types import ShippingRequest
from postmanpat.utils.graphs.stacked_bar import generate_stacked_bar_chart
from postmanpat.utils.time.is_day import is_day
from postmanpat.utils.upload.litterbox import upload_litter


async def get_countries_bar_chart(postie: Postie, all_mail: list[ShippingRequest]):
    is_daytime = is_day(
        city=postie.fields.city,
    )

    if is_daytime:
        text_colour = "black"
        bg_colour = "white"
    else:
        text_colour = "white"
        bg_colour = "#181A1E"

    countries = list(set([mail.fields.country for mail in all_mail]))

    status_categories = [
        ShippingReqStatus.pending,
        ShippingReqStatus.assigned,
        ShippingReqStatus.dispatched,
        ShippingReqStatus.mailed,
        ShippingReqStatus.arrived,
        ShippingReqStatus.errored,
    ]

    status_to_counts = {status: [0] * len(countries) for status in status_categories}

    for i, country in enumerate(countries):
        country_mails = [mail for mail in all_mail if mail.fields.country == country]
        for mail in country_mails:
            status_to_counts[mail.fields.status][i] += 1

    y = np.array([status_to_counts[status] for status in status_categories])
    x = np.arange(len(countries))

    colours = [
        "#C8C4E0",
        "#F4D3F9",
        "#FBEBBC",
        "#CCF3F0",
        "#D6F4D4",
        "#F4B994",
    ]

    b = BytesIO()
    fig = generate_stacked_bar_chart(
        x=x,
        y=y,
        labels=countries,
        text_colour=text_colour,
        bg_colour=bg_colour,
        categories=[status.name.capitalize() for status in status_categories],
        colours=colours,
        x_axis_label="Country",
    )
    fig.savefig(
        b, bbox_inches="tight", pad_inches=0.1, transparent=False, dpi=300, format="png"
    )

    url = await upload_litter(
        file=b.getvalue(),
        filename="mail_stats.png",
        expiry="1h",
        content_type="image/png",
    )
    caption = "Mail stats by country"

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
        "alt_text": caption,
    }
