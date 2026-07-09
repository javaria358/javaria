
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('student', 'Student'),
    ('admin', 'Administrator'),
]

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}))
    first_name = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), initial='student')
    admin_code = forms.CharField(
        required=False,
        label='Admin access code',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter admin signup code'}),
        help_text='Required only for administrator registration.',
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'admin_code',
            'password1',
            'password2',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username or staff ID'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()
            field.widget.attrs.setdefault('autocomplete', field_name)
        self.fields['role'].widget.attrs['class'] = 'form-check-input'
        self.fields['admin_code'].widget.attrs['placeholder'] = 'Enter admin signup code'

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        admin_code = cleaned_data.get('admin_code')
        if role == 'admin':
            expected_code = getattr(settings, 'ADMIN_SIGNUP_CODE', 'GCTW-ADMIN-2026')
            if admin_code != expected_code:
                self.add_error('admin_code', 'The admin signup code is incorrect.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if self.cleaned_data.get('role') == 'admin':
            user.is_staff = True
        if commit:
            user.save()
            # create or update profile role
            try:
                from .models import Profile
                profile, _ = Profile.objects.get_or_create(user=user)
                profile.role = self.cleaned_data.get('role', 'student')
                profile.save()
            except Exception:
                # if models aren't migrated yet, skip gracefully
                pass
        return user

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ("student", "Student"),
    ("admin", "Administrator"),
]


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "you@example.com"
        })
    )

    first_name = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "First Name"
        })
    )

    last_name = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Last Name"
        })
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        initial="student",
        widget=forms.RadioSelect()
    )

    admin_code = forms.CharField(
        required=False,
        label="Admin Access Code",
        help_text="Required only for Administrator registration.",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter Admin Signup Code"
        })
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Username"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Bootstrap styling
        for field_name, field in self.fields.items():

            if field_name == "role":
                continue

            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " form-control").strip()

        self.fields["role"].widget.attrs.update({
            "class": "form-check-input"
        })

    def clean(self):
        cleaned_data = super().clean()

        role = cleaned_data.get("role")
        admin_code = cleaned_data.get("admin_code")

        if role == "admin":
            expected_code = getattr(
                settings,
                "ADMIN_SIGNUP_CODE",
                "GCTW-ADMIN-2026"
            )

            if admin_code != expected_code:
                self.add_error(
                    "admin_code",
                    "Invalid administrator signup code."
                )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data.get("email")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")

        # Make administrator staff
        if self.cleaned_data.get("role") == "admin":
            user.is_staff = True

        if commit:
            user.save()

            # Save role in Profile model
            try:
                from .models import Profile

                profile, created = Profile.objects.get_or_create(
                    user=user
                )

                profile.role = self.cleaned_data.get("role")
                profile.save()

            except Exception:
                # Ignore if Profile model is not available
                pass

        return user

