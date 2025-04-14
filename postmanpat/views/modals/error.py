from typing import Any

from postmanpat.utils.env import env


def get_error_view(msg: str, traceback: str | None = None) -> dict[str, Any]:
    if traceback:
        msg = f"{msg}\n\nTraceback:\n```{traceback}```"
    return {
        "type": "modal",
        "callback_id": "error_view",
        "title": {
            "type": "plain_text",
            "text": "Error",
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"oh butter my crumpets, it looks like something broke, lemme go let <@{env.slack_maintainer_id}> know",
                },
            },
            {
                "type": "image",
                "image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/bed78abfcc64405c7d5a6014498db9c04c846c3a_postman-pat.gif",
                "alt_text": "👀",
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": msg},
            },
        ],
    }
