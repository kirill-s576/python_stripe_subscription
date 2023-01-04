from typing import List
from enum import Enum
import datetime
from pydantic import BaseModel, validator

from .price import StripeApiPrice


class StripeSubscriptionStatusEnum(Enum):

    incomplete = "incomplete"
    incomplete_expired = "incomplete_expired"
    trialing = "trialing"
    active = "active"
    past_due = "past_due"
    canceled = "canceled"
    unpaid = "unpaid"


class StripeSubscriptionCollectionMethodEnum(Enum):

    charge_automatically = "charge_automatically"
    send_invoice = "send_invoice"


class StripeApiSubscriptionItem(BaseModel):
    id: str
    quantity: int
    price: StripeApiPrice


class StripeApiSubscription(BaseModel):

    id: str
    customer: str
    default_payment_method: str = None
    days_until_due: int = None
    latest_invoice: str = None
    status: StripeSubscriptionStatusEnum
    collection_method: str = None
    created: datetime.datetime
    start_date: datetime.datetime = None
    ended_at: datetime.datetime = None
    canceled_at: datetime.datetime = None
    current_period_start: datetime.datetime = None
    current_period_end: datetime.datetime = None
    items: List[StripeApiSubscriptionItem] = []

    class Config:
        use_enum_values = True

    @validator("items", pre=True)
    def up_items(cls, v):
        return v["data"]

    def contains_price_id(self, price_id: str) -> bool:
        filtered = list(filter(lambda x: x.price.id == price_id, self.items))
        return len(filtered) > 0

    @property
    def active(self) -> bool:
        return self.status == StripeSubscriptionStatusEnum.active.value

    @validator('created')
    def created_replace_tz(cls, v):
        if v:
            return v.replace(tzinfo=None)

    @validator('start_date')
    def start_date_replace_tz(cls, v):
        if v:
            return v.replace(tzinfo=None)

    @validator('ended_at')
    def ended_at_replace_tz(cls, v):
        if v:
            return v.replace(tzinfo=None)

    @validator('canceled_at')
    def canceled_at_replace_tz(cls, v):
        if v:
            return v.replace(tzinfo=None)

    @validator('current_period_start')
    def current_period_start_replace_tz(cls, v):
        if v:
            return v.replace(tzinfo=None)

    @validator('current_period_end')
    def current_period_end_replace_tz(cls, v):
        if v:
            return v.replace(tzinfo=None)
