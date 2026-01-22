from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from subscriptions.models import UserSubscription
from django.forms.models import model_to_dict
from .models import Content
from rest_framework_simplejwt.authentication import JWTAuthentication


class ContentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return content list filtered by the user's subscription.
        - If the user's subscription is inactive -> 403
        - If the plan allows premium -> return all content
        - Otherwise -> return only non-premium content
        """
        # Ensure we derive the user from the authenticated token.
        user = getattr(request, 'user', None)
        if not user or getattr(user, 'is_anonymous', True):
            # Try to validate JWT from Authorization header explicitly
            try:   

                jwt_auth = JWTAuthentication()
                auth_header = request.META.get('HTTP_AUTHORIZATION', '')
                if auth_header.startswith('Bearer '):
                    raw_token = auth_header.split()[1]
                    validated = jwt_auth.get_validated_token(raw_token)
                    user = jwt_auth.get_user(validated)
            except Exception:
                user = None

        if not user:
            return Response({"error": "Authentication credentials were not provided."}, status=401)

        try:
            print(f"USER:{user}")
            subscription = UserSubscription.objects.get(user=user)
            # print all key/value pairs of the subscription for debugging
            try:
                print("subscription:", model_to_dict(subscription))
            except Exception:
                print("subscription:", subscription.__dict__)

        except UserSubscription.DoesNotExist:
            return Response({"error": "No subscription"}, status=403)

        if not subscription.is_active:
            return Response({"error": "Subscription inactive"}, status=403)
        print(f"plan: {type(subscription.plan)}")
        if subscription.plan.name=='paid':
            items = Content.objects.all()
        else:
            items = Content.objects.filter(is_premium=False)

        data = [
            {"id": c.id, "title": c.title, "is_premium": c.is_premium}
            for c in items
        ]

        return Response({"content": data})
