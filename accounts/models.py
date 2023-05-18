from django.db import models
from django.contrib.auth.models import User

from task_manager.models import CodingTask

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    completed_tasks = models.ManyToManyField(CodingTask, blank=True)

    class Meta:
        app_label = 'accounts'