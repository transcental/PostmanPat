import logging
import traceback
from typing import Any

from slack_sdk.web.async_client import AsyncWebClient

from postmanpat.utils.env import env
from postmanpat.utils.logging import send_heartbeat
from postmanpat.views.home.error import get_error_view
from postmanpat.views.home.loading import get_loading_view
from postmanpat.views.home.manage_mail import get_manage_mail_view
from postmanpat.views.home.manage_posties import get_manage_posties_view
from postmanpat.views.home.manager import get_manager_view
from postmanpat.views.home.postie import get_postie_view
from postmanpat.views.home.unknown_user import get_unknown_user_view


async def on_app_home_opened(event: dict[str, Any], client: AsyncWebClient):
    user_id = event["user"]
    await open_app_home("default", client, user_id)


async def open_app_home(home_type: str, client: AsyncWebClient, user_id: str):
    try:
        await client.views_publish(view=get_loading_view(), user_id=user_id)

        user = env.airtable_client.get_postie_by_slack_id(user_id)

        if not user:
            user_info = await client.users_info(user=user_id) or {}
            name = (
                user_info.get("user", {}).get("profile", {}).get("display_name")
                or user_info.get("user", {}).get("profile", {}).get("real_name")
                or "person"
            )
            view = get_unknown_user_view(name)
        else:
            logging.info(f"Opening {home_type} for {user_id}")
            match home_type:
                case "default" | "dashboard":
                    if user.is_manager:
                        view = get_manager_view(user)
                    else:
                        view = get_postie_view(user)
                case "manage-posties":
                    view = await get_manage_posties_view(user)
                case "manage-mail":
                    view = await get_manage_mail_view(user)
                case _:
                    await send_heartbeat(
                        f"Attempted to load unknown app home type {home_type} for <@{user_id}>"
                    )
                    view = get_error_view(
                        f"This shouldn't happen, please tell <@{env.slack_maintainer_id}> that app home case `_` was hit with home type `{home_type}`"
                    )
    except Exception as e:
        logging.error(f"Error opening app home: {e}")
        tb = traceback.format_exception(e)

        tb_str = "".join(tb)

        view = get_error_view(
            f"An error occurred while opening the app home: {e}",
            traceback=tb_str,
        )
        err_type = type(e).__name__
        await send_heartbeat(
            f"`{err_type}` opening app home for <@{user_id}>",
            messages=[f"```{tb_str}```", f"cc <@{env.slack_maintainer_id}>"],
        )

    await client.views_publish(user_id=user_id, view=view)
