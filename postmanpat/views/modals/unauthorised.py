from typing import Any


def get_unauthorised_view(name: str) -> dict[str, Any]:
    return {
        "type": "modal",
        "callback_id": "unauthorised",
        "title": {
            "type": "plain_text",
            "text": "Unauthorised",
            "emoji": True,
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":shiba-alert: hey {name}, you, what are you doing here.\nskeddadle.\n\ni'm not joking around kiddo, scram, get outta here.\nthis ain't your turf, it's mine",
                },
            },
        ],
    }
