from django import template
from checkout.models import BillingForm

register = template.Library()

@register.filter
def crispy(user):
    #billingForm = BillingForm.objects.filter(user = user)
    pass
    		