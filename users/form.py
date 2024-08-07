from django import forms
from .models import AppUsers

class AppUserForm(forms.ModelForm):
    class Meta:
        model =AppUsers
        fields = ["name", "pwd", "occupation"]
        widgets = {
            'pwd': forms.PasswordInput(),
        }
