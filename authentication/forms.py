from django import forms
from .models import candAccount, cands

class candAccountForm(forms.ModelForm):
    class Meta:
        model = candAccount
        fields = ('candID', 'username', 'password')
        
class candidate(forms.ModelForm):
    class Meta:
        model = cands
        fields = ('cv','fname','address','military_status','phone','dob')