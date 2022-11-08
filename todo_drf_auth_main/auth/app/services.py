from datetime import datetime, timezone

import jwt
from django.conf import settings
from django.db import transaction


def check_password(last_pwd_update):
    """
    Check password expiration
    :param last_pwd_update: datetime
    :return: bool
    """
    time_past = datetime.now(tz=timezone.utc) - last_pwd_update
    if time_past > settings.PASSWORD_UPDATE_PERIOD:
        return False
    return True


def check_user(user):
    """

    :param user:
    :return:
    """

    if not check_password(user.last_pwd_update):
        return "Password expired"

    return "OK"


def change_password(user, new_password):
    """
    :param user: object User
    :param new_password
    """
    with transaction.atomic():
        user.set_password(new_password)
        user.last_pwd_update = datetime.now(tz=timezone.utc)
        user.save()


def generate_token(user, exp_time, token_type="access"):
    expire_date = round((datetime.now(tz=timezone.utc) + exp_time).timestamp())

    body = {
        "token_type": token_type,
        "exp": expire_date,
        "user_id": user.id,
        "email": user.email,
        "username": user.username,
        "is_superuser": user.is_superuser,
        "is_staff": user.is_staff,
    }
    encoded_body = jwt.encode(
        body, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_body


def verify_token(token, token_type):
    """Check token"""
    try:
        decoded_jwt = jwt.decode(
            token, settings.SECRET_KEY, algorithms=(settings.JWT_ALGORITHM,)
        )
    except (
        jwt.exceptions.ExpiredSignatureError,
        jwt.exceptions.InvalidSignatureError,
        jwt.exceptions.DecodeError,
    ):
        return None

    if decoded_jwt["token_type"] != token_type:
        return None

    return decoded_jwt
