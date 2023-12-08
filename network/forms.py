from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'status', 'gender', 'profile_picture']

    # Add this field to handle the username
    username = forms.CharField(max_length=100, widget=forms.HiddenInput())  

    def clean_username(self):
        return self.cleaned_data['username']