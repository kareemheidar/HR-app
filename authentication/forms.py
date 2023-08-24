from django import forms
from .models import candidate_account, candidate,human_resources,CV

class candAccountForm(forms.ModelForm):
    class Meta:
        model = candidate_account
        fields = ('candID', 'username', 'password')
        
class candidate(forms.ModelForm):
    class Meta:
        model = candidate
        fields = ('fname', 'lname', 'email', 'phone', 'address', 'gender', 'military_status', 'cand_status', 'dob', 'cv', 'jobID')
        

class human_resources(forms.ModelForm):
    class Meta:
        model = human_resources       
        fields = ('HR_code','username','password')
        
        
class candidate_account(forms.ModelForm):
    class Meta:
        model = candidate_account       
        fields = ('candID','username','password')
        
class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ('University','Major','Education','LinkedIn','Work_Experience','SoftSkill','TechSkill','AddNote')