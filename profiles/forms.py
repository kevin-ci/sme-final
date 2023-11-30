from django import forms
from .models import UserProfile, Job

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

class JobForm(forms.ModelForm):
    company_name = forms.CharField(label='Company Name', required=True)

    class Meta:
        model = Job
        fields = ('title', 'description', 'start_date', 'end_date')
        labels = {
            'title': 'Job Title',
            'end_date': 'End Date (if finished)',
        }
        
    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
        self.fields['end_date'].widget = forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
        field_order = [
            'company_name',
            'title',
            'description',
            'start_date',
            'end_date',
        ]
        self.fields = {field_name: self.fields[field_name] for field_name in field_order}
        
class SignupForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        label='Your name',
        widget=forms.TextInput(attrs={'placeholder': 'John Smith'})
    )
    headline = forms.CharField(
        max_length=50,
        label='Your profile headline',
        widget=forms.TextInput(attrs={'placeholder': 'Software Developer'})
    )    
    def signup(self, request, user):
        user.refresh_from_db()
        user.profile.name = self.cleaned_data['name']
        user.profile.headline = self.cleaned_data['headline']
        user.save()