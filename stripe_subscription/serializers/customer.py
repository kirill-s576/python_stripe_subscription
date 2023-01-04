from pydantic import BaseModel, validator
from typing import Union
import datetime


class StripeApiCustomer(BaseModel):
    id: str
    email: str
    object: str
    balance: int
    created: Union[int, datetime.datetime]
    name: str = None
    phone: str = None
    address: dict = None
    description: str = None
    currency: str = None

    @validator('created')
    def created_to_dt(cls, value: int):
        return datetime.datetime.fromtimestamp(value)
