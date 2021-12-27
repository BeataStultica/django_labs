from django.db import models
from django.utils.timezone import now


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    responsibilities = models.CharField(max_length=255)
    orders = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
