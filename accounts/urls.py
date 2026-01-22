from django.urls import path
from .views import (
    LoginView,
    LogoutDeviceView,
    LogoutAllDevicesView,
    RegisterView,
    CustomTokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/device/', LogoutDeviceView.as_view(), name='logout-device'),
    path('logout/all/', LogoutAllDevicesView.as_view(), name='logout-all'),
]
