from django.db import models

from apps.projectsapp.models import Project


class Lead(models.Model):
    sender_fullname = models.CharField(max_length=100, blank=False, null=False)
    sender_email = models.EmailField(blank=False, null=False)
    subject = models.CharField(max_length=120, blank=True, null=True)
    message = models.TextField(max_length=500, blank=False, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sender_fullname
