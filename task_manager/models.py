import os
from django.db import models
from django.db.models.signals import post_delete

def delete_files(sender, instance, **kwargs):
    if instance.markdown_file:
        os.remove(instance.markdown_file.path)
    if instance.test_file:
        os.remove(instance.test_file.path)
    if instance.initial_file:
        os.remove(instance.initial_file.path)

class CodingTask(models.Model):
    description = models.CharField(max_length=200)
    markdown_file = models.FileField(upload_to='markdown/', null=True, blank=True)
    test_file = models.FileField(upload_to='testing/', null=True, blank=True)
    initial_file = models.FileField(upload_to='initials/', null=True, blank=True)

post_delete.connect(delete_files, sender=CodingTask)