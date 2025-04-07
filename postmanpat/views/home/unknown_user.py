def get_unknown_user_view(name: str):
    return {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f":postman-pat: Hey there {name}!",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Aww, looks like I don't have anything for you today. Sorry!",
                },
            },
        ],
    }
