
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': True}
        self.helper.layout = Layout(
Field('username'),
            Field('password'),
            Submit('login', 'Login', css_class='w-100 mt-2 mb-2'),
        )


class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        required = ('username', 'password', 'first_name', 'last_name', 'email')
        widgets = {'password': forms.PasswordInput}
        help_texts = dict(username=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

        self.helper = FormHelper()
        self.helper.attrs = dict(novalidate=True)
        self.helper.layout = Layout(
Field('username'),
            Field('password'),
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            Submit('signup', 'Sign up', css_class='btn-info w-100 mt-2 mb-2'),
        )

    def clean_email(self):
        email = self.cleaned_data['email']

        if self._meta.model.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('A user with that email already exists.')

        return email

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user = super().save(*args, **kwargs)
        return user
