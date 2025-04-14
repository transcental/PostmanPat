from typing import Any


def get_accept_invite_view(user_id: str, private_metadata: str) -> dict[str, Any]:
    return {
        "type": "modal",
        "callback_id": "accept-invite",
        "title": {"type": "plain_text", "text": "Mail Team", "emoji": True},
        "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
        "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Accept your invitation!",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "heya! i'm so glad you decided to accept your invitation to join mail team :D\nbefore we can get started though, got a bit of paperwork for ya to do. sorry bout that, i know it's boring but it'll be done soon!",
                },
            },
            {
                "type": "input",
                "block_id": "first-name",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "first-name",
                    "placeholder": {"type": "plain_text", "text": "Patrick"},
                },
                "label": {"type": "plain_text", "text": "First Name", "emoji": True},
            },
            {
                "type": "input",
                "block_id": "last-name",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "last-name",
                    "placeholder": {"type": "plain_text", "text": "Clifton"},
                },
                "label": {"type": "plain_text", "text": "Last Name", "emoji": True},
            },
            {
                "type": "input",
                "block_id": "email",
                "element": {
                    "type": "email_text_input",
                    "action_id": "email",
                    "placeholder": {"type": "plain_text", "text": "pat@hackclub.com"},
                },
                "label": {"type": "plain_text", "text": "Email", "emoji": True},
            },
            {
                "type": "input",
                "block_id": "on-hiatus",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hell yeah!",
                                "emoji": True,
                            },
                            "value": "no",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Sorry, I'm on hiatus",
                                "emoji": True,
                            },
                            "value": "yes",
                        },
                    ],
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": "Hell yeah!",
                            "emoji": True,
                        },
                        "value": "no",
                    },
                    "action_id": "on-hiatus",
                },
                "label": {
                    "type": "plain_text",
                    "text": "Do you want to start sending mail straight away?",
                    "emoji": True,
                },
            },
            {
                "type": "input",
                "block_id": "address-line-1",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "address-line-1",
                    "placeholder": {"type": "plain_text", "text": "Forge Cottage"},
                },
                "label": {
                    "type": "plain_text",
                    "text": "Address Line 1",
                    "emoji": True,
                },
            },
            {
                "type": "input",
                "block_id": "address-line-2",
                "optional": True,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "address-line-2",
                    "placeholder": {"type": "plain_text", "text": "Unit 2"},
                },
                "label": {
                    "type": "plain_text",
                    "text": "Address Line 2",
                    "emoji": True,
                },
            },
            {
                "type": "input",
                "block_id": "address-line-3",
                "optional": True,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "address-line-3",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Phone: +44 07700 900123",
                    },
                },
                "label": {
                    "type": "plain_text",
                    "text": "Address Line 3",
                    "emoji": True,
                },
            },
            {
                "type": "input",
                "block_id": "city",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "city",
                    "placeholder": {"type": "plain_text", "text": "Greendale"},
                },
                "label": {"type": "plain_text", "text": "City", "emoji": True},
            },
            {
                "type": "input",
                "block_id": "county",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "county",
                    "placeholder": {"type": "plain_text", "text": "Cumbria"},
                },
                "label": {"type": "plain_text", "text": "County", "emoji": True},
            },
            {
                "type": "input",
                "block_id": "postcode",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "postcode",
                    "placeholder": {"type": "plain_text", "text": "CA10 3PP"},
                },
                "label": {"type": "plain_text", "text": "Postcode", "emoji": True},
            },
            {
                "type": "input",
                "block_id": "country",
                "element": {
                    "type": "external_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "United Kingdom",
                        "emoji": True,
                    },
                    "action_id": "country",
                    "min_query_length": 0,
                },
                "label": {"type": "plain_text", "text": "Country", "emoji": True},
            },
            {
                "type": "input",
                "block_id": "currency",
                "element": {
                    "type": "external_select",
                    "placeholder": {"type": "plain_text", "text": "GBP", "emoji": True},
                    "action_id": "currency",
                    "min_query_length": 0,
                },
                "label": {
                    "type": "plain_text",
                    "text": "What currency do you use?",
                    "emoji": True,
                },
            },
            {
                "type": "input",
                "block_id": "price-per-domestic-letter",
                "element": {
                    "type": "number_input",
                    "is_decimal_allowed": True,
                    "action_id": "price-per-domestic-letter",
                    "placeholder": {"type": "plain_text", "text": "0.87"},
                },
                "label": {
                    "type": "plain_text",
                    "text": "How much does a domestic letter cost? (Use your local currency)",
                    "emoji": True,
                },
            },
            {
                "type": "input",
                "block_id": "price-per-international-letter",
                "element": {
                    "type": "number_input",
                    "is_decimal_allowed": True,
                    "action_id": "price-per-international-letter",
                    "placeholder": {"type": "plain_text", "text": "3.20"},
                },
                "label": {
                    "type": "plain_text",
                    "text": "How much does an international letter cost? (Use your local currency)",
                    "emoji": True,
                },
            },
        ],
        "private_metadata": private_metadata,
    }
