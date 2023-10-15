from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from authentication.models import CustomUser
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeCheckoutView(APIView):
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1O0RfcSGKyiP0qJkeQzGPJ1e',
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card',],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )

            return redirect(checkout_session.url)
        except:
            return Response(
                {'error': 'Something went wrong when creating stripe checkout session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class UserPremium(APIView):
    def post(self, request):
        username = request.data.get('username')

        try:
            user = CustomUser.objects.get(username=username)
            user.is_premium = True
            user.save()
            return Response({'message': f'{username} is now a premium user.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': f'User with username {username} not found.'}, status=status.HTTP_404_NOT_FOUND)