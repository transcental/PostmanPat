from postmanpat.utils.airtable.types import Postie
from postmanpat.utils.airtable.types import ShippingReqStatus
from postmanpat.utils.env import env
from postmanpat.views.home.components.buttons import get_buttons


def get_manager_view(postie: Postie):
    reqs = env.airtable_client.get_requests(formula="'{{status}}' != 'draft'")
    if not reqs:
        reqs = []

    organised_reqs = {}
    for req in reqs:
        status = req.fields.status
        if status not in organised_reqs:
            organised_reqs[status] = []
        organised_reqs[status].append(req)
    formatted_msg = f"""
    *Requests*
    {len(reqs)} requests found
    {len(organised_reqs.get(ShippingReqStatus.pending.value, []))} pending
    {len(organised_reqs.get(ShippingReqStatus.assigned.value, []))} assigned
    {len(organised_reqs.get(ShippingReqStatus.dispatched.value, []))} dispatched
    {len(organised_reqs.get(ShippingReqStatus.mailed.value, []))} mailed
    {len(organised_reqs.get(ShippingReqStatus.arrived.value, []))} arrived
    {len(organised_reqs.get(ShippingReqStatus.errored.value, []))} errored
    """

    btns = get_buttons(postie, "dashboard")

    return {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "Postman Pat", "emoji": True},
            },
            btns,
            {"type": "divider"},
            {"type": "section", "text": {"type": "mrkdwn", "text": formatted_msg}},
        ],
    }
