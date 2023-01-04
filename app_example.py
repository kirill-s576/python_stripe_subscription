from stripe_subscription.sub_service import StripeSubscriptionService


CUSTOMER_EMAIL = "email@gmail.com"
STRIPE_API_KEY = "stripe_api_key"


stripe_service = StripeSubscriptionService(
    api_key=STRIPE_API_KEY
)
customer, customer_created = stripe_service.get_or_create_customer(
    email=CUSTOMER_EMAIL
)
print("Operation: Create customer. Customer:", customer, "Created:", customer_created)

price, price_created = stripe_service.get_or_create_price(
    "TEST_9",
    799,
    recurring_count=1,
    year_interval=False
)
print("Operation: Create price. Price: ", price, "Created: ", price_created)

payment_method, method_created = stripe_service.get_or_create_payment_method(
    customer_email=CUSTOMER_EMAIL,
    card_number="5200828282828210",
    exp_month=11,
    exp_year=2023,
    cvc="608"
)
print("Operation: Create payment method. Payment method: ", payment_method, "Created: ", method_created)

subscription = stripe_service.create_subscription_if_not_exist(
    customer=customer,
    price=price
)
print("Operation: Create subscription. Subscription: ", subscription)
