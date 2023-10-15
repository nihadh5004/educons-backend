from django.urls import path
from .views import *


urlpatterns = [
    path('create-checkout-session', StripeCheckoutView.as_view()),
    path('user-premium/', UserPremium.as_view()),
]