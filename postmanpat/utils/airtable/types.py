from enum import Enum

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
    manager: bool = False


class Postie(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    fields: PostieFields


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
    postie: str | None = None


class ShippingRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    fields: ShippingRequestFields
