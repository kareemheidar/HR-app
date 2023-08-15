from django import forms
from .models import candAccount, candidate

class candAccountForm(forms.ModelForm):
    class Meta:
        model = candAccount
        fields = ('candID', 'username', 'password')
        
class candidate(forms.ModelForm):
    class Meta:
        model = candidate
        fields = ('cv','fname','address','military-status','phone','dob')