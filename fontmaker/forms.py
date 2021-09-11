from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Proj, HUser


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class ProjForm(forms.ModelForm):
    class Meta:
        model = Proj
        fields = ("name", "isK")

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')

        if name == '':
            raise ValidationError("name is empty")

        proj = Proj.objects.filter(name=name)
        if proj.exists():
            raise ValidationError("Project name already exists")
