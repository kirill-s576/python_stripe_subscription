from typing import Tuple
from stripe_subscription.base_api import (
    StripeCustomerApi,
    StripePaymentMethodApi,
    StripeProductApi,
    StripePriceApi,
    StripeSubscriptionApi
)
from stripe_subscription.serializers import (
    StripeApiCustomer,
    StripeApiPrice,
    StripePriceRecurring,
    StripePriceRecurringIntervalEnum,
    StripePaymentMethod,
    StripeApiSubscription
)
from stripe_subscription.exceptions import ActiveSubscriptionFoundException


class StripeSubscriptionService:

    """
    Class which specified for Payments Service necessaries.
    How to subscribe user:
    1. Create User -> self.get_or_create_customer(email: str)
        This method returns created or exists user.
    2. Create Price -> self.get_or_create_price(
         product_name: str,
         amount: int,
         recurring_count: int = 1000,
         year_interval: bool = False
        )
        Into Stripe logic Price = Plan.
        Method returns exist Price by product_name or new Price.
    3. Create Payment method for charging money for subscription.
    4. Create Subscription.
    """

    def __init__(
        self,
        api_key: str
    ) -> None:
        self.customer_api = StripeCustomerApi(api_key=api_key)
        self.payment_method_api = StripePaymentMethodApi(api_key=api_key)
        self.product_api = StripeProductApi(api_key=api_key)
        self.price_api = StripePriceApi(api_key=api_key)
        self.subscription_api = StripeSubscriptionApi(api_key=api_key)

    def get_or_create_customer(
        self,
        email: str
    ) -> Tuple[StripeApiCustomer, bool]:
        """
        Method creates customer into StripeAPI.
        Method pipeline:
            1.Check if customer exists.
            2.Create if not.
            3.Return customer.
        :returns (customer: StripeApiCustomer, created: bool)
        """
        user = self.customer_api.get_by_email(email=email)
        if user:
            return user, False
        user = self.customer_api.create(email=email)
        return user, True

    def get_or_create_price(
        self,
        product_name: str,
        amount: int,
        recurring_count: int = 1000, # How many times get money.
        year_interval: bool = False # Default interval is month. Set True for year subscription.
    ) -> Tuple[StripeApiPrice, bool]:
        """
        Method pipeline:
            1.Check if price exists. If yes return price.
            else
            2.Check if product with the same name exists.
            3.Create if not.
            4.Create price with product.
            5.Return created price.
        :returns Tuple[StripeApiPrice, bool] - (StripeApiPrice, is_created)
        """
        rc = f"{recurring_count}_times"
        yi = f"{'yearly' if year_interval else 'monthly'}"
        product_name = f"{product_name}_{amount}_{rc}_{yi}"
        price = self.price_api.get_by_lookup_key(lookup_key=product_name)
        if price:
            return price, False
        product = self.product_api.get_by_name(name=product_name)
        if not product:
            product = self.product_api.create(name=product_name)
        recurring = StripePriceRecurring(
            interval=StripePriceRecurringIntervalEnum.year if year_interval else StripePriceRecurringIntervalEnum.month,
            interval_count=recurring_count
        )
        price = self.price_api.create(
            amount=amount,
            product=product,
            recurring=recurring
        )
        return price, True

    def get_or_create_payment_method(
            self,
            customer_email: str,
            card_number: str,
            exp_month: int,
            exp_year: int,
            cvc: str
    ) -> Tuple[StripePaymentMethod, bool]:
        """
        :param customer_email: str
        :param card_number: str
        :param exp_month: int
        :param exp_year: int
        :param cvc: cvc
        Function pipeline
            1. Get or create customer from API by email.
            1. Check for exists payment_method into Customer's methods list.
            2. Create PaymentMethod if not, retrieve if exists.
            3. Attach Customer to PaymentMethod if created.
        :return: StripePaymentMethod, created: bool
        """
        customer, created = self.get_or_create_customer(email=customer_email)
        customer_methods = self.payment_method_api.list(
            customer_id=customer.id
        )
        if exp_year < 100:
            exp_year = exp_year + 2000
        filtered_methods = list(filter(
            lambda method: (
                    method.card.exp_month == exp_month and
                    method.card.exp_year == exp_year and
                    method.card.last4 == card_number[-4:]
            ), customer_methods
        ))
        if filtered_methods:
            filtered_methods.sort(key = lambda x: x.created, reverse=True)
            method = filtered_methods[0]
            if len(filtered_methods) > 1:
                for method in filtered_methods[:-1]:
                    self.payment_method_api.detach_from_customer(
                        method_id=method.id
                    )
            return method, False

        payment_method = self.payment_method_api.create(
            card_number=card_number,
            exp_month=exp_month,
            exp_year=exp_year,
            cvc=cvc
        )
        attached_payment_method = self.payment_method_api.attach_to_customer(
            customer=customer,
            payment_method=payment_method
        )
        self.payment_method_api.stripe.Customer.modify(
            customer.id,
            invoice_settings={
                "default_payment_method": payment_method.id
            }
        )
        return attached_payment_method, True

    def create_subscription_if_not_exist(
        self,
        customer: StripeApiCustomer,
        price: StripeApiPrice
    ) -> StripeApiSubscription:
        """
        1. Check for existing and active subscription.
        2. If exists - Raise Exception
        3. If not - Create and return
        """
        customer_subs = self.subscription_api.get_customer_subscriptions(
            customer_id=customer.id
        )
        filtered_customer_subs = list(filter(
            lambda x: x.contains_price_id(price.id) == True, customer_subs
        ))
        if filtered_customer_subs:
            filtered_customer_subs.sort(key=lambda x: x.created, reverse=True)
            sub = filtered_customer_subs[0]
            if sub.active:
                raise ActiveSubscriptionFoundException(
                    "Customer has active subscription for this product"
                )
        subscription = self.subscription_api.create(
            price=price,
            customer=customer
        )
        return subscription

    def get_customer_subscriptions(
            self,
            customer_email: str
    ):
        customer, created = self.get_or_create_customer(email=customer_email)
        customer_subs = self.subscription_api.get_customer_subscriptions(
            customer_id=customer.id
        )
        return customer_subs

    def retrieve_subscription(
            self,
            subscription_id: str
    ):
        sub = self.subscription_api.retrieve(
            subscription_id=subscription_id
        )
        return sub