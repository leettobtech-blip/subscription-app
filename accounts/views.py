from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from subscriptions.models import UserSubscription, SubscriptionPlan
from .models import Device, User
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.throttling import ScopedRateThrottle



class LoginView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        device_id = request.data.get('device_id')

        user = authenticate(email=email, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        subscription = UserSubscription.objects.get(user=user)
        # Ensure subscription expiry is enforced before proceeding
        try:
            subscription.check_and_update_active()
        except Exception:
            pass
        # Handle same-device re-login: update existing Device instead of creating duplicate.
        existing_device = None
        if device_id:
            existing_device = Device.objects.filter(user=user, device_id=device_id).first()

        if existing_device:
            # Rotate refresh token for this device and return tokens (idempotent for same device)
            refresh = RefreshToken.for_user(user)
            existing_device.refresh_token = str(refresh)
            existing_device.save(update_fields=['refresh_token'])
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "detail": "Login successful (device refreshed)"
            })

        # New device: enforce device limit
        active_devices = Device.objects.filter(user=user).count()
        if not subscription.is_active:
            return Response({"error": "Subscription inactive"}, status=status.HTTP_403_FORBIDDEN)

        if active_devices >= subscription.plan.max_devices:
            return Response(
                {"error": "Device limit reached"},
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)

        Device.objects.create(
            user=user,
            device_id=device_id,
            refresh_token=str(refresh)
        )

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "detail": "Login successful"
        })

# class LogoutDeviceView(APIView):
#     def post(self, request):
#         device_id = request.data.get("device_id")
#         Device.objects.filter(
#             user=request.user,
#             device_id=device_id
#         ).delete()
#         return Response({"message": "Logged out from device"})

class LogoutAllView(APIView):
    def post(self, request):
        Device.objects.filter(user=request.user).delete()
        return Response({"message": "Logged out from all devices"})


class LogoutDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "refresh token required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass

        Device.objects.filter(
            user=request.user,
            refresh_token=refresh_token
        ).delete()

        return Response({"message": "Device logged out"})
        

class LogoutAllDevicesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        Device.objects.filter(user=request.user).delete()

        return Response({"message": "Logged out from all devices"})



class RegisterView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'register'
    """Create a new user, create a default free subscription plan if needed,
    attach a `UserSubscription`, and return JWT tokens.
    """
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "email and password required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "user exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email=email, password=password)

        plan, _ = SubscriptionPlan.objects.get_or_create(
            name="Free",
            defaults={"max_devices": 1, "price": 0},
        )
        UserSubscription.objects.create(user=user, plan=plan)

        # Do not issue JWTs at registration. User should authenticate via
        # the login endpoint to receive access/refresh tokens.
        return Response({"detail": "User created"}, status=status.HTTP_201_CREATED)


class CustomTokenRefreshView(TokenRefreshView):
    """Extend TokenRefreshView to update the stored device refresh token when rotation occurs.

    Expects the request body to contain the current refresh token. If a `Device`
    record exists with that refresh token, it will be updated to the new refresh
    token returned by SimpleJWT.
    """
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'token_refresh'

    def post(self, request, *args, **kwargs):
        old_refresh = request.data.get('refresh')
        response = super().post(request, *args, **kwargs)
        # When rotation is enabled, SimpleJWT returns a new `refresh` token
        new_refresh = None
        try:
            new_refresh = response.data.get('refresh')
        except Exception:
            new_refresh = None

        if old_refresh and new_refresh:
            Device.objects.filter(refresh_token=old_refresh).update(refresh_token=new_refresh)

        return response

