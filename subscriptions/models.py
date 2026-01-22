from django.db import models

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    max_devices = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # whether this plan gives access to premium content
    allows_premium = models.BooleanField(default=False)
    # duration of subscription in days (used when user subscribes)
    duration_days = models.IntegerField(default=30)

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    # subscription period
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def check_and_update_active(self):
        """Check expiry and update `is_active` if needed. Returns current active state."""
        from django.utils import timezone

        if self.end_date:
            now = timezone.now()
            if self.is_active and self.end_date < now:
                self.is_active = False
                self.save(update_fields=['is_active'])
        return self.is_active
