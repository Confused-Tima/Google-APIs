from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserForm(UserCreationForm):
    """User creation form (uses built-in UserCreationForm)"""

    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "*Your first name.."}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "*Your last name.."}),
    )
    username = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "*Email.."}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "*Password..",
                "class": "password",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "*Confirm Password..",
                "class": "password",
            }
        )
    )

    # reCAPTACHA Token
    token = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class AuthForm(AuthenticationForm):
    """Built-in Authentication form using User model"""

    username = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "*Email.."}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "*Password..",
                "class": "password",
            }
        )
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )


class UserProfileForm(forms.ModelForm):
    """
    Basic model form for our user profile model, that extends built-in User.
    """

    address = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput)
    town = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput)
    county = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput)
    post_code = forms.CharField(max_length=8, required=True, widget=forms.HiddenInput)
    country = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput)
    longitude = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput)
    latitude = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput)

    class Meta:
        model = UserProfile
        fields = (
            "address",
            "town",
            "county",
            "post_code",
            "country",
            "longitude",
            "latitude",
        )
