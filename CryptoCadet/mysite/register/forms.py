from django.contrib.auth import login, authenticate, password_validation
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from validate_email import validate_email

from main.models import Profile

from main.models import Address


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not validate_email(email):
            raise ValidationError(u'Please enter a valid and existing email address.')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')
        if password1 and username and password1.lower() == username.lower():
            raise ValidationError("Your password can’t be too similar to your username.")
        password_validation.validate_password(password1)
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password1 = self.cleaned_data.get('password1')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        if commit:
            user.save()
            profile = Profile(user=user)
            profile.save()
            address = Address(user=user)
            address.save()
        return user

class PersonalInfoForm(forms.ModelForm):
    address = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    class Meta:
        model = Profile
        fields = ['address', 'phone_number']

        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'account_balance': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        profile = super(PersonalInfoForm, self).save(commit=False)
        profile.address = self.cleaned_data.get('address')
        profile.phone_number = self.cleaned_data.get('phone_number')
        if commit:
            profile.save()
        return profile

class AddressForm(forms.ModelForm):
    city = forms.CharField(max_length=100, required=True)
    street_name = forms.CharField(max_length=100, required=True)
    post_code = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=100, required=True)
    class Meta:
        model = Address
        fields = ['city', 'street_name', 'post_code', 'country']

        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'street_name': forms.TextInput(attrs={'class': 'form-control'}),
            'post_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def save(self, commit=True):
        address = super(AddressForm, self).save(commit=False)
        address.city = self.cleaned_data.get('city')
        address.street_name = self.cleaned_data.get('street_name')
        address.post_code = self.cleaned_data.get('post_code')
        address.country = self.cleaned_data.get('country')
        if commit:
            address.save()
        return address