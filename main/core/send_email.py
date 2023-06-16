from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def send_email_varification(activation_link, user):
    message = f"Click to verificate your email \n{activation_link}?user_id={user.id}&confirmation_token={default_token_generator.make_token(user)}"
    send_mail(
        "Email verification",
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
