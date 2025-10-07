from .models import Paywall


def payment_context(request):
    """Makes the first Paywall record available globally."""
    payment = Paywall.objects.first()
    return {"paywall": payment}
