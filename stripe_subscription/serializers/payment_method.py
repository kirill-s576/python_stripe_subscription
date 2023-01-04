from pydantic import BaseModel
import datetime


class StripePaymentMethodCard(BaseModel):
    exp_month: int
    exp_year: int
    last4: str


class StripePaymentMethod(BaseModel):

    id: str
    customer: str = None
    type: str
    created: datetime.datetime
    card: StripePaymentMethodCard = None
