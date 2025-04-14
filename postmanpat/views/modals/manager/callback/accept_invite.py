from slack_bolt.async_app import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from postmanpat.utils.env import env


async def accept_invite_callback(ack: AsyncAck, body, client: AsyncWebClient):
    await ack()
    view = body.get("view")
    user_id = body["user"]["id"]
    values = view["state"]["values"]
    first_name = values["first-name"]["first-name"]["value"]
    last_name = values["last-name"]["last-name"]["value"]
    email = values["email"]["email"]["value"]
    on_hiatus = values["on-hiatus"]["on-hiatus"]["selected_option"]["value"]
    address_line_1 = values["address-line-1"]["address-line-1"]["value"]
    address_line_2 = values["address-line-2"]["address-line-2"]["value"]
    address_line_3 = values["address-line-3"]["address-line-3"]["value"]
    city = values["city"]["city"]["value"]
    county = values["county"]["county"]["value"]
    postcode = values["postcode"]["postcode"]["value"]
    country = values["country"]["country"]["selected_option"]["value"]
    price_per_domestic_letter = values["price-per-domestic-letter"][
        "price-per-domestic-letter"
    ]["value"]
    price_per_international_letter = values["price-per-international-letter"][
        "price-per-international-letter"
    ]["value"]
    currency = values["currency"]["currency"]["selected_option"]["value"]
    private_metadata = view["private_metadata"]
    inviter = private_metadata.split("-")[0]

    role = private_metadata.split("-")[1]

    inviter_postie = env.airtable_client.get_postie_by_slack_id(inviter)

    fields = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "on_hiatus": True if on_hiatus == "yes" else False,
        "address_line_1": address_line_1,
        "address_line_2": address_line_2,
        "address_line_3": address_line_3,
        "city": city,
        "county": county,
        "postcode": postcode,
        "country": country,
        "local_price_per_domestic_letter": float(price_per_domestic_letter),
        "local_price_per_intl_letter": float(price_per_international_letter),
        "local_currency": currency,
        "role": role,
        "invited_by": [inviter_postie.id] if inviter_postie else None,
        "slack_id": user_id,
        "exchange_rate": "1.0",
        "usd_price_per_domestic_letter": float(price_per_domestic_letter),
        "usd_price_per_intl_letter": float(price_per_international_letter),
    }
    postie = env.airtable_client.create_postie(fields)

    if postie:
        await client.chat_postMessage(
            channel=user_id,
            text=f"hey! welcome to the mail team! <@{inviter}> invited you to join as a {role}, you should speak to them for more information about what you need to do.\n\nhave a good one - pat :)",
        )
        await client.chat_postMessage(
            channel=inviter,
            text=f"hey! <@{user_id}> has accepted your invite to join the mail team as a {role}!\n\ncheerio - pat :)",
        )
