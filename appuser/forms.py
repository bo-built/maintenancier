from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autocomplete': 'off'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'off',
            'id': 'id_login_password',
        })
    )


class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name',
            'autocomplete': 'off',
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name',
            'autocomplete': 'off',
        })
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autocomplete': 'off',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a password',
            'autocomplete': 'off',
            'minlength': 9,
            'maxlength': 75,
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'autocomplete': 'off',
            'minlength': 9,
            'maxlength': 75,
        })
    )


class changePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your current password',
            'autocomplete': 'off',
            'minlength': 9,
            'maxlength': 75,
        })
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a new password',
            'autocomplete': 'off',
            'minlength': 9,
            'maxlength': 75,
        })
    )

    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your new password',
            'autocomplete': 'off',
            'minlength': 9,
            'maxlength': 75,
        })
    )


class UserProfileForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name',
            'autocomplete': 'off',
            'x-model': 'profile.first_name',
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name',
            'autocomplete': 'off',
            'x-model': 'profile.last_name',
        })
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autocomplete': 'off',
            'x-model': 'profile.email',
        })
    )