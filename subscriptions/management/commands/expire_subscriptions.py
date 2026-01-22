from django.core.management.base import BaseCommand
from django.utils import timezone
from subscriptions.models import UserSubscription


class Command(BaseCommand):
    help = 'Expire user subscriptions whose end_date has passed'

    def handle(self, *args, **options):
        now = timezone.now()
        qs = UserSubscription.objects.filter(is_active=True, end_date__lt=now)
        count = qs.count()
        for sub in qs:
            sub.is_active = False
            sub.save(update_fields=['is_active'])
        self.stdout.write(self.style.SUCCESS(f'Expired {count} subscriptions'))
