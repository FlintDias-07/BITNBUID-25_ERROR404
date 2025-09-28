from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role']
            )
        return user

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Profile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

class NotificationPreferencesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'email_projects', 'email_bids', 'email_messages', 'email_payments',
            'push_messages', 'push_bids'
        ]
        widgets = {
            'email_projects': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_bids': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_messages': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_payments': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'push_messages': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'push_bids': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PlatformPreferencesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['theme', 'language', 'profile_public', 'show_online_status']
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-select'}),
            'language': forms.Select(attrs={'class': 'form-select'}),
            'profile_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_online_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }