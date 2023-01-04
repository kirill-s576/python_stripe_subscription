class StripeApiCustomException(Exception):
    pass


class ActiveSubscriptionFoundException(StripeApiCustomException):
    pass
