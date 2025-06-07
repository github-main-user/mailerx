import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

logger = logging.getLogger(__name__)

User = get_user_model()


def send_verification_email(request, user) -> None:
    """Created and sends a verification token by email."""

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = request.build_absolute_uri(
        reverse("users:verify_email", kwargs={"uidb64": uid, "token": token})
    )
    subject = "Verify your email"
    message = f"Click the link to verify your email: {verification_link}"

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    logger.info("Sent verification email on %s", user.email)


def activate_user(uidb64: str, token: str) -> bool:
    """
    Verifies given token, if it is valid - activates user.
    Returns status of the verification.
    """

    try:
        logger.info("Tring to decode an email verification token")
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        logger.error("Error during email verification token decoding")
        return False

    if user.is_active:
        logger.info("User %s is already activated", user.pk)
        return True

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        logger.info("User %s is successfully activated %s", user.pk)
        return True

    logger.warning("Given email verification token is not valid")
    return False
