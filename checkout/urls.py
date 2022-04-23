from django.urls import path 
from . views import checkout,paymenthandler, charge, oderView,paynow

app_name = "checkout"

urlpatterns = [
	path('checkout/', checkout, name="index"),
 	path('paynow/', paynow, name="paynow"),
 	#path('paymenthandler/',paymenthandler, name='paymenthandler'),
	#path('payment/', payment, name="payment"),
	path('charge/', charge, name="charge"),
	path('my-orders/', oderView, name="oderView")
]