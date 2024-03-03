import stripe
from django.conf import settings
from django.core.exceptions import ValidationError

from item.models import Item


def get_checkout(data: dict):
    item = data['item']
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': item.price,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url="http://" + data["domain"] + '/success/',
            cancel_url="http://" + data["domain"] + "/fail/",
        )

    except Exception as e:
        raise ValidationError({"error": str(e)})
    return checkout_session
