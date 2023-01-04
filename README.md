# Python Stripe subscription package.

Implements a case for managing customer's subscriptions without Stripe checkout page.
It uses approach with credit card data we send to Stripe.

    Pay attention it's not safe way to work with Stipe.
    More accurate way to use Stripe checkout page.
    Use this article to get example with checkout page within Django app.
    https://dev.to/documatic/integrate-stripe-payments-with-django-by-building-a-digital-products-selling-app-le5


## Main points.

1. Main class which implements business logic is ```stripe_subscription.sub_service.StripeSubscriptionService```
2. ```stripe_subscription.async_sub_service.AsyncStripeSubscriptionService``` duplicates methods of the same class 
but with async pattern with using ThreadPool executor.
3. Package uses types with validation provided by Pydantic library. Serializers are objects 
which represent data structure of Stripe API objects.
4. Explanation of methods sense provided by Docstrings.
5. app_example.py provides demo workflow.


## Stripe API Official documentation

https://stripe.com/docs/api