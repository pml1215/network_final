from django.db import models


class Email(models.Model):
    to_email = models.TextField()
    cc_email = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return self.subject

