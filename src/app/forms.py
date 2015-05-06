from app.models import UserProfile
from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text="Please use your comapany email")
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('department',)
        
class ReportFilterForm(forms.Form):
    from_date = forms.DateField(label='From date')
    to_date = forms.DateField(label='To date')