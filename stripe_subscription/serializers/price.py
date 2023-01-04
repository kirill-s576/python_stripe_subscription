from pydantic import BaseModel
from enum import Enum


class StripeCurrencies(Enum):
    """
    StripeCurrencies
    """
    usd = "usd"


class StripePriceRecurringIntervalEnum(Enum):
    """
    StripePriceRecurringIntervalEnum
    """
    day = "day"
    week = "week"
    month = "month"
    year = "year"


class StripePriceRecurring(BaseModel):
    """
    StripePriceRecurring
    """
    interval: StripePriceRecurringIntervalEnum = StripePriceRecurringIntervalEnum.month
    interval_count: int = 1

    class Config:
        use_enum_values = True


class StripeApiPrice(BaseModel):
    """
    StripeApiPrice
    """
    id: str
    unit_amount: int
    currency: StripeCurrencies = StripeCurrencies.usd
    recurring: StripePriceRecurring
    product: str
    active: bool = True

    class Config:
        use_enum_values = True
