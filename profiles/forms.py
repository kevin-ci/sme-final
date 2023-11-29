from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        
class SignupForm(forms.Form):
    name = forms.CharField(max_length=50, label='Your name')
    headline = forms.CharField(max_length=50, label='Your profile headline')
    
    def signup(self, request, user):
        user.refresh_from_db()
        user.profile.name = self.cleaned_data['name']
        user.profile.headline = self.cleaned_data['headline']
        user.save()