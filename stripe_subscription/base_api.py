import stripe
from typing import Optional, List

from stripe_subscription.serializers import (
    StripeApiProduct,
    StripeApiCustomer,
    StripeApiSubscription,
    StripeApiSession,
    StripePaymentMethod,
    StripeApiPrice,
    StripeCurrencies,
    StripePriceRecurring
)


class StripeApi:

    def __init__(
        self,
        api_key: str
    ) -> None:
        """
        :param api_key: str - Api Key
        """
        self.stripe = stripe
        self.stripe.api_key = api_key


class StripeCustomerApi(StripeApi):

    def get_by_id(
        self,
        customer_id: str
    ) -> Optional[StripeApiCustomer]:
        """

        """
        response = self.stripe.Customer.retrieve(customer_id)
        customer = StripeApiCustomer(**response)
        return customer

    def get_by_email(
        self,
        email: str
    ) -> Optional[StripeApiCustomer]:
        """

        """
        result = self.stripe.Customer.list(email=email)
        if result["data"]:
            customer = StripeApiCustomer(**result["data"][0])
            return customer
        return None

    def create(
        self,
        email: str
    ) -> StripeApiCustomer:
        """

        """
        response = self.stripe.Customer.create(
            email = email
        )
        customer = StripeApiCustomer(**response)
        return customer

    def delete(
        self,
        customer_id: str
    ) -> bool:
        """

        """
        response = self.stripe.Customer.delete(
            customer_id
        )
        return response["deleted"]

    def get_payment_methods(
        self,
        customer: StripeApiCustomer
    ) -> List[StripePaymentMethod]:
        """

        """
        result = self.stripe.PaymentMethod.list(
            customer=customer.id
        )
        return [StripePaymentMethod(**method_dict) for method_dict in result["data"]]


class StripePaymentMethodApi(StripeApi):

    def create(
        self,
        card_number: str,
        exp_month: int,
        exp_year: int,
        cvc: str
    ) -> StripePaymentMethod:
        """

        """

        response = self.stripe.PaymentMethod.create(
            type="card",
            card={
                "number": card_number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": cvc,
            }
        )
        payment_method = StripePaymentMethod(**response)
        return payment_method

    def list(
            self,
            customer_id: str
    ) -> List[StripePaymentMethod]:
        result = self.stripe.PaymentMethod.list(
            customer=customer_id,
            type = 'card'
        )
        methods = [
            StripePaymentMethod(**method) for method in result["data"]
        ]
        return methods

    def attach_to_customer(
        self,
        payment_method: StripePaymentMethod,
        customer: StripeApiCustomer
    ) -> StripePaymentMethod:
        """

        """
        response = self.stripe.PaymentMethod.attach(
            payment_method.id, customer=customer.id
        )
        payment_method = StripePaymentMethod(**response)
        return payment_method

    def detach_from_customer(self, method_id: str) -> StripePaymentMethod:
        response = self.stripe.PaymentMethod.detach(
            method_id
        )
        payment_method = StripePaymentMethod(**response)
        return payment_method

class StripeProductApi(StripeApi):

    @classmethod
    def __get_product_url_by_name(
            cls,
            name: str
    ):
        """

        """
        return f"{name.replace(' ', '')}"

    def create(
            self,
            name: str
    ) -> StripeApiProduct:
        """

        """
        response = self.stripe.Product.create(
            name=name,
            url=f"https://{self.__get_product_url_by_name(name)}"
        )
        product = StripeApiProduct(**response)
        return product

    def get_by_id(
            self,
            product_id: str
    ) -> StripeApiProduct:
        """

        """
        result = self.stripe.Product.retrieve(product_id)
        product = StripeApiProduct(**result)
        return product

    def get_by_name(
            self,
            name: str
    ) -> Optional[StripeApiProduct]:
        """

        """
        result = self.stripe.Product.list(
            url=f"https://{self.__get_product_url_by_name(name)}"
        )
        if result["data"]:
            customer = StripeApiProduct(**result["data"][0])
            return customer
        return None

    def delete(
            self,
            product_id: str
    ) -> bool:
        """

        """
        response = self.stripe.Product.delete(product_id)
        return response["deleted"]


class StripePriceApi(StripeApi):

    def create(
        self,
        amount: int,
        product: StripeApiProduct,
        recurring: StripePriceRecurring,
        currency: StripeCurrencies = StripeCurrencies.usd
    ) -> StripeApiPrice:
        data = {
            "lookup_key": product.name,
            "unit_amount": int(amount),
            "currency": currency.value,
            "recurring": recurring.dict(),
            "product": product.id
        }
        response = self.stripe.Price.create(**data)
        price = StripeApiPrice(**response)
        return price

    def get_by_lookup_key(
        self,
        lookup_key: str
    ) -> Optional[StripeApiPrice]:
        """
        :param lookup_key: It's product name if price was created by this package.
        """
        result = self.stripe.Price.list(lookup_keys=[lookup_key])
        if result["data"]:
            customer = StripeApiPrice(**result["data"][0])
            return customer
        return None

    def update_amount(
            self,
            price_id: str,
            new_amount: int,
            product_name: str
    ) -> StripeApiPrice:
        response = self.stripe.Price.modify(
            price_id,
            lookup_key=None,
            active=False
        )
        new_price_data = {
            "lookup_key": product_name,
            "unit_amount": int(new_amount),
            "currency": response["currency"],
            "recurring": response["recurring"],
            "product": response["product"]
        }
        response = self.stripe.Price.create(**new_price_data)
        price = StripeApiPrice(**response)
        return price


class StripeSubscriptionApi(StripeApi):

    def create(
        self,
        customer: StripeApiCustomer,
        price: StripeApiPrice
    ) -> StripeApiSubscription:
        """

        """
        response = self.stripe.Subscription.create(
            customer=customer.id,
            items=[
                {"price": price.id},
            ],
        )
        subscription = StripeApiSubscription(**response)
        return subscription

    def get_customer_subscriptions(
            self,
            customer_id: str
    ) -> List[StripeApiSubscription]:
        response = self.stripe.Subscription.list(
            customer = customer_id
        )
        return [
            StripeApiSubscription(**sub) for sub in response["data"]
        ]

    def create_checkout_session(
        self,
        success_url: str,
        cancel_url: str,
        customer: StripeApiCustomer,
        price: StripeApiPrice
    ) -> StripeApiSession:
        """
        Returns StripeApiSession.
        """
        result = self.stripe.checkout.Session.create(
            success_url=success_url,
            cancel_url=cancel_url,
            payment_method_types=['card'],
            mode='subscription',
            line_items=[
                {
                    'price': price.id,
                    'quantity': 1
                },
            ],
            customer=customer.id
        )
        serializer = StripeApiSession(**result)
        return serializer

    def retrieve(self, subscription_id: str) -> Optional[StripeApiSubscription]:
        response = self.stripe.Subscription.retrieve(
            subscription_id
        )
        if not response:
            return None
        sub = StripeApiSubscription(**response)
        return sub
