import asyncio

from postmanpat.utils.env import env
from postmanpat.utils.logging import send_heartbeat


async def update_rates_loop():
    await update_rates()
    await asyncio.sleep(3600)


async def update_rates():
    """
    Update the exchange rates for all posties in the database.
    """
    await send_heartbeat("Updating exchange rates")
    posties = env.airtable_client.get_posties()
    try:
        async with env.session.get(
            "https://api.frankfurter.dev/v1/latest?base=USD"
        ) as res:
            data = await res.json()
    except Exception as e:
        await send_heartbeat(f"Failed to fetch exchange rates: {e}")
        return
    rates = data["rates"]

    updates = []
    for postie in posties:
        if postie.fields.local_currency != "USD":
            exchange_rate = rates.get(postie.fields.local_currency)
            domestic_price = postie.fields.local_price_per_domestic_letter
            international_price = postie.fields.local_price_per_intl_letter
            if exchange_rate:
                postie.fields.exchange_rate = exchange_rate
                postie.fields.usd_price_per_domestic_letter = (
                    domestic_price / exchange_rate
                )
                postie.fields.usd_price_per_intl_letter = (
                    international_price / exchange_rate
                )

                updates.append(
                    {
                        "id": postie.id,
                        "fields": {
                            "exchange_rate": str(exchange_rate),
                            "usd_price_per_domestic_letter": domestic_price
                            / exchange_rate,
                            "usd_price_per_intl_letter": international_price
                            / exchange_rate,
                        },
                    }
                )
    if updates:
        env.airtable_client.update_posties(updates)
        await send_heartbeat("Exchange rates updated successfully")
