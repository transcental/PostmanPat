import logging
import traceback

from slack_sdk.web.async_client import AsyncWebClient

from postmanpat.utils.env import env
from postmanpat.utils.logging import send_heartbeat
from postmanpat.views.modals.error import get_error_view
from postmanpat.views.modals.loading import get_loading_view
from postmanpat.views.modals.superadmin.invite_manager import get_invite_manager_view
from postmanpat.views.modals.unauthorised import get_unauthorised_view


async def open_view(
    view_type: str, client: AsyncWebClient, user_id: str, trigger_id: str
):
    view_id = None
    try:
        view_res = await client.views_open(
            view=get_loading_view(), user_id=user_id, trigger_id=trigger_id
        )
        view_id = view_res.get("view", {}).get("id", None)
        if not view_id:
            raise Exception("Failed to open loading view")

        user = env.airtable_client.get_postie_by_slack_id(user_id)

        user_info = await client.users_info(user=user_id) or {}
        name = (
            user_info.get("user", {}).get("profile", {}).get("display_name")
            or user_info.get("user", {}).get("profile", {}).get("real_name")
            or "person"
        )
        if not user:
            view = get_unauthorised_view(name)
        else:
            logging.info(f"Opening modal {view_type} for {user_id}")
            auth = False
            if view_type.startswith("superadmin"):
                if user.is_superadmin:
                    auth = True
            elif view_type.startswith("admin"):
                if user.is_manager:
                    auth = True
            else:
                auth = True

            if not auth:
                view = get_unauthorised_view(name)

            match view_type:
                case "superadmin-invite-manager":
                    view = get_invite_manager_view()
                case _:
                    await send_heartbeat(
                        f"Attempted to load unknown modal type `{view_type}` for <@{user_id}>"
                    )
                    view = get_error_view(
                        f"whoopsies, `open_view` case `_` was hit with type `{view_type}`"
                    )
    except Exception as e:
        logging.error(f"Error opening view: {e}")
        tb = traceback.format_exception(e)

        tb_str = "".join(tb)

        view = get_error_view(
            f"An error occurred while opening the view `{view_type}`: `{e}`",
            traceback=tb_str,
        )
        err_type = type(e).__name__
        await send_heartbeat(
            f"`{err_type}` opening view `{view_type}` for <@{user_id}>",
            messages=[f"```{tb_str}```", f"cc <@{env.slack_maintainer_id}>"],
        )

    try:
        await client.views_update(user_id=user_id, view=view, view_id=view_id)
    except Exception as e:
        logging.error(f"Error updating view: {e}")
        tb = traceback.format_exception(e)

        tb_str = "".join(tb)
        err_type = type(e).__name__

        await send_heartbeat(
            f"`{err_type}` opening view `{view_type}` for <@{user_id}>",
            messages=[f"```{tb_str}```", f"cc <@{env.slack_maintainer_id}>"],
        )
