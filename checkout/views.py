#import stripe
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from cart.models import Order, Cart
from . models import BillingForm, BillingAddress
from django.views.generic.base import TemplateView
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def homepage(request):
	currency = 'INR'
	amount = 2000 # Rs. 200

	# Create a Razorpay Order
	razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
	razorpay_order_id = razorpay_order['id']
	callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
	context = {
		
	}
	context['razorpay_order_id'] = razorpay_order_id
	context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
	context['razorpay_amount'] = amount
	context['currency'] = currency
	context['callback_url'] = callback_url
	return render(request, 'payment.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is None:
				amount = 50000 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()

def paynow(request):
	currency = 'INR'
	form = BillingForm
	
	order_qs = Order.objects.filter(user= request.user, ordered=False)
	order_items = order_qs[0].orderitems.all()
	order_total = order_qs[0].get_totals() 
	context = {"form": form, "order_items": order_items, "order_total": order_total}
	# Getting the saved saved_address
	saved_address = BillingAddress.objects.filter(user = request.user)
	order_qs = Order.objects.filter(user= request.user, ordered=False)
	order_total = order_qs[0].get_totals() 
	totalCents = float(order_total * 100);
	total = round(totalCents, 2)
	      #request.POST['amount']
	amount = total
	# Create a Razorpay Order
	razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
	razorpay_order_id = razorpay_order['id']
	callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
	context = {
		
	}
	context['razorpay_order_id'] = razorpay_order_id
	context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
	context['razorpay_amount'] = amount
	context['currency'] = currency
	context['callback_url'] = callback_url
	return render(request, 'checkout/payment.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is None:
				amount = 50000 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()


#stripe.api_key = settings.STRIPE_SECRET_KEY 

def checkout(request):
    
	# Checkout view
	form = BillingForm
	
	order_qs = Order.objects.filter(user= request.user, ordered=False)
	order_items = order_qs[0].orderitems.all()
	order_total = order_qs[0].get_totals() 
	context = {"form": form, "order_items": order_items, "order_total": order_total}
	# Getting the saved saved_address
	saved_address = BillingAddress.objects.filter(user = request.user)
	if saved_address.exists():
		savedAddress = saved_address.first()
		context = {"form": form, "order_items": order_items, "order_total": order_total, "savedAddress": savedAddress}
	if request.method == "POST":
		saved_address = BillingAddress.objects.filter(user = request.user)
		if saved_address.exists():

			savedAddress = saved_address.first()
			form = BillingForm(request.POST, instance=savedAddress)
			if form.is_valid():
				billingaddress = form.save(commit=False)
				billingaddress.user = request.user
				billingaddress.save()
		else:
			form = BillingForm(request.POST)
			if form.is_valid():
				billingaddress = form.save(commit=False)
				billingaddress.user = request.user
				billingaddress.save()
				
	return render(request, 'checkout/index.html', context)




#def payment(request):
	#key = settings.STRIPE_PUBLISHABLE_KEY
	#order_qs = Order.objects.filter(user= request.user, ordered=False)
	#order_total = order_qs[0].get_totals() 
	#totalCents = float(order_total * 100);
	#total = round(totalCents, 2)
	#if request.method == 'POST':
		#charge = stripe.Charge.create(amount=total,
            #currency='usd',
            #description=order_qs,
            #source=request.POST['stripeToken'])
		#print(charge)
        
	#return render(request, 'checkout/payment.html', {"key": key, "total": total})




def charge(request):
	order = Order.objects.get(user=request.user, ordered=False)
	orderitems = order.orderitems.all()
	order_total = order.get_totals() 
	totalCents = int(float(order_total * 100))
	if request.method == 'POST':
		charge = stripe.Charge.create(amount=totalCents,
            currency='inr',
            description=order,
            source=request.POST['stripeToken'])
		print(charge)
		if charge.status == "succeeded":
			orderId = get_random_string(length=16, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
			print(charge.id)
			order.ordered = True
			order.paymentId = charge.id
			order.orderId = f'#{request.user}{orderId}'
			order.save()
			cartItems = Cart.objects.filter(user=request.user)
			for item in cartItems:
				item.purchased = True
				item.save()
		return render(request, 'checkout/charge.html', {"items": orderitems, "order": order })



def oderView(request):

	try:
		orders = Order.objects.filter(user=request.user, ordered=True)
		context = {
			"orders": orders
		}
	except:
		messages.warning(request, "You do not have an active order")
		return redirect('/')
	return render(request, 'checkout/order.html', context)