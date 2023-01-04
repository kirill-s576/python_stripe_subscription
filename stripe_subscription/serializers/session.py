from pydantic import BaseModel
from enum import Enum


class StripePaymentStatusEnum(Enum):
    paid = "paid"
    unpaid = "unpaid"
    no_payment_required = "no_payment_required"


class StripeApiSession(BaseModel):
    id: str
    url: str
    cancel_url: str
    success_url: str
    payment_intent: str = None
    payment_status: StripePaymentStatusEnum = None
    customer: str = None
    customer_email: str = None
    amount_total: int = None
