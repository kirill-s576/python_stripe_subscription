# Python Stripe subscription package.

Implements a case for managing customer's subscriptions without Stripe checkout page.
It uses approach with card data we send to Stripe.

## Main points.

1. Main class which implements business logic is ```stripe_subscription.sub_service.StripeSubscriptionService```
2. ```stripe_subscription.async_sub_service.AsyncStripeSubscriptionService``` duplicates methods of the same class 
but with async pattern with using ThreadPool executor.
3. Package uses types with validation provided by Pydantic library.
4. Explanation of methods sense provided by Docstrings.
5. app_example.py provides demo workflow.