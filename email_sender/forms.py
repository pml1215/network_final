from django import forms
from .models import Email


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['to_email', 'cc_email', 'subject', 'body', 'attachment']
