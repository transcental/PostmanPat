from typing import Any


def get_loading_view() -> dict[str, Any]:
    return {
        "type": "modal",
        "callback_id": "loading_view",
        "title": {
            "type": "plain_text",
            "text": ":hourglass: Loading...",
            "emoji": True,
        },
        "blocks": [
            {
                "type": "image",
                "image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/605ffb061f87eb5f7865575b24330e5d30f70dc5_stitch-sad.gif",
                "alt_text": "loading... (ft stitch)",
            }
        ],
    }
