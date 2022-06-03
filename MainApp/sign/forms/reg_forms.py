from django import forms
from main.models import UserModel


class RegistrationForm:
    """Registration form"""
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    telegram_chat_id = forms.IntegerField(required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = UserModel
        fields = [
            'username', 'first_name', 'last_name', 'password', 'confirm_password',
            'phone', 'telegram_chat_id', 'email', "profile_picture"
        ]