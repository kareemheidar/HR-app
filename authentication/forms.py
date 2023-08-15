from django import forms
from .models import candAccount

class candAccountForm(forms.ModelForm):
    class Meta:
        model = candAccount
        fields = ('candID', 'username', 'password')