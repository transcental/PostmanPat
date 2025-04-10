from enum import Enum
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class PostieFields(BaseModel):
    model_config = ConfigDict(extra="allow")
    identifier: str
    slack_id: str
    first_name: str
    last_name: str
    email: EmailStr
    on_hiatus: bool = False
    address_line_1: str
    address_line_2: str | None = None
    address_line_3: str | None = None
    city: str
    county: str
    country: str
    postcode: str
    address: str
    local_price_per_domestic_letter: float
    local_price_per_intl_letter: float
    local_currency: str
    exchange_rate: str
    usd_price_per_domestic_letter: float
    usd_price_per_intl_letter: float
    post: list[str] = []
    autonumber: int
    role: Literal["postie", "manager", "superadmin"] = "postie"
    created_at: str
    updated_at: str
    invited_by: list[str]


class Postie(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    fields: PostieFields

    @property
    def is_manager(self) -> bool:
        return self.fields.role in ["manager", "superadmin"]

    @property
    def is_regular_manager(self) -> bool:
        return self.fields.role == "manager"

    @property
    def is_superadmin(self) -> bool:
        return self.fields.role == "superadmin"

    @property
    def is_working(self) -> bool:
        return not self.fields.on_hiatus

    @property
    def inviter(self) -> Optional["Postie"]:
        from postmanpat.utils.env import env

        inviter = self.fields.invited_by
        posties = env.airtable_client.get_posties_by_ids(inviter)
        if posties:
            return posties[0]
        else:
            return None


class ShippingReqStatus(Enum):
    pending = "pending_assignment"
    assigned = "assigned"
    dispatched = "dispatched"
    mailed = "mailed"
    arrived = "arrived"
    errored = "errored"
    draft = "draft"


class ShippingRequestFields(BaseModel):
    identifier: str
    email: EmailStr
    first_name: str
    last_name: str
    address_line_1: str
    address_line_2: str | None = None
    address_line_3: str | None = None
    city: str
    county: str
    country: str
    postcode: str
    address: str
    status: ShippingReqStatus
    process_request: bool = False
    autonumber: int
    tracking_number: str | None = None
    shipping_cost: float | None = None
    service_used: str | None = None
    contents: list[str] = []
    skus: list[str] = []
    custom_instructions: str | None = None
    postie: list[str] | None = None


class ShippingRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    fields: ShippingRequestFields

    @property
    def is_sent(self) -> bool:
        return self.fields.status in [
            ShippingReqStatus.mailed,
            ShippingReqStatus.arrived,
        ]

    @property
    def has_arrived(self) -> bool:
        return self.fields.status == ShippingReqStatus.arrived

    @property
    def postie(self) -> str | None:
        return self.fields.postie[0] if self.fields.postie else None
