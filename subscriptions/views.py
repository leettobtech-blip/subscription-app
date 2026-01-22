from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import UserSubscription, SubscriptionPlan

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class UserSubscriptionView(View):
	"""Return the current authenticated user's subscription as JSON.

	- Returns 401 if the user is not authenticated.
	- Returns 404 if the user has no subscription.
	"""
	def get(self, request, *args, **kwargs):
		user = request.user
		if not user or not user.is_authenticated:
			return JsonResponse({"detail": "Authentication credentials were not provided."}, status=401)

		try:
			subscription = UserSubscription.objects.select_related('plan').get(user=user)
		except UserSubscription.DoesNotExist:
			return JsonResponse({"detail": "Not found."}, status=404)

		data = {
			"plan": subscription.plan.name,
			"is_active": subscription.is_active,
			"max_devices": subscription.plan.max_devices,
			"price": str(subscription.plan.price),
		}
		return JsonResponse(data)


class SubscribeView(APIView):
	"""Allow an authenticated user to subscribe to a plan.

	POST body:
	  { "plan_id": <int> }

	This is a simple stub that simulates a payment flow and creates/updates
	the user's `UserSubscription`. In a real system this would call a
	payment gateway and record invoices.
	"""
	permission_classes = [IsAuthenticated]

	def post(self, request, *args, **kwargs):
		# Always use the authenticated user from the token; ignore any `user` field
		# sent by the client to prevent spoofing.
		if 'user' in request.data:
			# ignore silently or you could log this event
			request.data.pop('user')

		plan_id = request.data.get('plan_id')
		if not plan_id:
			return Response({"error": "plan_id is required"}, status=status.HTTP_400_BAD_REQUEST)

		try:
			plan = SubscriptionPlan.objects.get(id=plan_id)
		except SubscriptionPlan.DoesNotExist:
			return Response({"error": "plan not found"}, status=status.HTTP_404_NOT_FOUND)

		# Create or update subscription
		# Use `request.user` derived from the authenticated token. Set
		# subscription period based on plan.duration_days.
		from django.utils import timezone
		from datetime import timedelta

		now = timezone.now()
		start = now
		end = now + timedelta(days=getattr(plan, 'duration_days', 30))

		subscription, created = UserSubscription.objects.update_or_create(
			user=request.user,
			defaults={
				'plan': plan,
				'is_active': True,
				'start_date': start,
				'end_date': end,
			}
		)

		data = {
			"plan": subscription.plan.name,
			"is_active": subscription.is_active,
			"max_devices": subscription.plan.max_devices,
			"price": str(subscription.plan.price),
		}

		return Response(data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
