from typing import Any

from slack_sdk.web.async_client import AsyncWebClient

from postmanpat.utils.env import env
from postmanpat.views.home.manager import get_manager_view
from postmanpat.views.home.postie import get_postie_view
from postmanpat.views.home.unknown_user import get_unknown_user_view


async def on_app_home_opened(event: dict[str, Any], client: AsyncWebClient):
    user_id = event["user"]

    user = env.airtable_client.get_postie_by_slack_id(user_id)

    if not user:
        user_info = await client.users_info(user=user_id) or {}
        name = (
            user_info.get("user", {}).get("profile", {}).get("display_name")
            or user_info.get("user", {}).get("profile", {}).get("real_name")
            or "person"
        )
        view = get_unknown_user_view(name)
    elif user.fields.manager:
        view = get_manager_view(user)
    else:
        view = get_postie_view(user)

    await client.views_publish(user_id=user_id, view=view)
