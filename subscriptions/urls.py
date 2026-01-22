from django.urls import path
from .views import UserSubscriptionView, SubscribeView

urlpatterns = [
    path('me/', UserSubscriptionView.as_view(), name='my-subscription'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
]

