import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
from stripe_subscription.sub_service import StripeSubscriptionService


class AsyncStripeSubscriptionService:

    """
    Async wrapper for StripeSubscriptionService.

    """

    EXECUTOR = ThreadPoolExecutor(max_workers=5)

    def __init__(self, api_key):
        self.api_key = api_key
        self.sync_service = StripeSubscriptionService(api_key)

    async def get_or_create_customer(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.EXECUTOR, functools.partial(
                self.sync_service.get_or_create_customer,
                *args,
                **kwargs
            )
        )

    async def get_or_create_price(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.EXECUTOR, functools.partial(
                self.sync_service.get_or_create_price,
                *args,
                **kwargs
            )
        )

    async def get_or_create_payment_method(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.EXECUTOR, functools.partial(
                self.sync_service.get_or_create_payment_method,
                *args,
                **kwargs
            )
        )

    async def create_subscription(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.EXECUTOR, functools.partial(
                self.sync_service.create_subscription_if_not_exist,
                *args,
                **kwargs
            )
        )

    async def get_customer_subscriptions(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.EXECUTOR, functools.partial(
                self.sync_service.get_customer_subscriptions,
                *args,
                **kwargs
            )
        )

    async def retrieve_subscription(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.EXECUTOR, functools.partial(
                self.sync_service.retrieve_subscription,
                *args,
                **kwargs
            )
        )
