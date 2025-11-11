from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from stalas.models import Baudejas, DatingStatuses
from django.contrib.auth.password_validation import validate_password

class SignupForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Slaptaraktis",
        widget=forms.PasswordInput,
        validators=[validate_password],

    )
    password2 = forms.CharField(
        label="Patvirtinkite slaptažodį",
        widget=forms.PasswordInput,
    )

    dating_status = forms.ChoiceField(
        label="Susitikinėjimo statusas",
        choices=DatingStatuses.choices,
        widget=forms.RadioSelect()
    )

    favourite_colour = forms.CharField(
        label="Mėgstamiausia spalva",
        widget=forms.TextInput,
        required=True,
    )

    class Meta:
        model = Baudejas
        fields = ["username", "email", "dating_status", "favourite_colour"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_dating_status(self):
        if self.cleaned_data["dating_status"] == "kompliktuota":
            raise forms.ValidationError("Invalid submission")
        return self.cleaned_data["dating_status"]

    def clean_favourite_colour(self):
        if self.cleaned_data["favourite_colour"].lower() == "geltona":
            raise forms.ValidationError("Invalid submission")
        return self.cleaned_data["favourite_colour"]

    def clean_password2(self):
        pw1 = self.cleaned_data.get("password1")
        pw2 = self.cleaned_data.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords don’t match")
        return pw2

    def save(self, commit=True):
        baudejas = super().save(commit=False)
        baudejas.set_password(self.cleaned_data["password1"])
        if commit:
            baudejas.save()
        return baudejas


class LoginForm(forms.Form):
    username = forms.CharField(label="Vartotojas", max_length=150, required=True)
    password = forms.CharField(label="Pusslaptraktis", widget=forms.PasswordInput, required=True)

    class Meta:
        model = Baudejas
        fields = ["username", "password"]

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            try:
                baudejas = Baudejas.objects.get(username=username)
            except Baudejas.DoesNotExist:
                raise forms.ValidationError("Vartotojas neegzistuoja")

            if not baudejas.check_password(password):
                raise forms.ValidationError("Kažką primalei tu čia")

            self.user = baudejas

        return self.cleaned_data
