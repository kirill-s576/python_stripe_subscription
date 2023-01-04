from pydantic import BaseModel


class StripeApiProduct(BaseModel):

    id: str
    name: str
    url: str
