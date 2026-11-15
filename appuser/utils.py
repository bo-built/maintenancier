from django.contrib.auth.models import User


def email_is_unique(email):
    email_in_use = User.objects.filter(email__iexact=email).first()
    return not email_in_use


def validate_password_strength(password):
    errors = []
    is_valid = True
    is_long_enough = False
    contains_upper = False
    contains_lower = False
    contains_number = False
    contains_no_spaces = True
    contains_special = False
    if len(password) >= 9:
        is_long_enough = True
    for char in password:
        if char.isupper():
            contains_upper = True
        if char.islower():
            contains_lower = True
        if char.isnumeric():
            contains_number = True
        if char.isspace():
            contains_no_spaces = False
        if not char.isalnum() and not char.isspace():
            contains_special = True

    if not is_long_enough:
        is_valid = False
        errors.append('Password must be at least 9 characters')

    if not contains_upper:
        is_valid = False
        errors.append('Password must contain at least one uppercase letter')

    if not contains_lower:
        is_valid = False
        errors.append('Password must contain at least one lowercase letter')

    if not contains_number:
        is_valid = False
        errors.append('Password must contain at least one number')

    if not contains_special:
        is_valid = False
        errors.append('Password must contain at least one special character')

    if not contains_no_spaces:
        is_valid = False
        errors.append('Password cannot have spaces')

    return is_valid, errors
