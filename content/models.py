from django.db import models

class Content(models.Model):
    title = models.CharField(max_length=200)
    is_premium = models.BooleanField(default=False)

