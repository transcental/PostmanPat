def get_error_view(msg: str):
    return {
        "type": "home",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Sorry, something went wrong. Please try again later.",
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Error message: {msg}"},
            },
        ],
    }
