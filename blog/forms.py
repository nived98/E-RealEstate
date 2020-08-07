from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from blog.models import UserProfile


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', ]


def save(self, commit=True):
    user_details = self.instance
    user_details.first_name = self.cleaned_data['first_name']
    user_details.last_name = self.cleaned_data['last_name']
    user_details.email = self.cleaned_data['email']
    user_details.user_phone = self.cleaned_data['user_phone']
    user_details.user_address = self.cleaned_data['user_address']
    user_details.user_city = self.cleaned_data['user_city']
    user_details.user_zipcode = self.cleaned_data['user_zipcode']

    # if self.cleaned_data['image']:
    #     property_listings.image = self.cleaned_data['image']

    if commit:
        user_details.save()
        return user_details
