from django.core.mail import send_mail
from django.template import loader
from rest_framework import status
from rest_framework.response import Response

from BookShop.settings import EMAIL_HOST_USER


def SendMail(code, email):
    html_message = loader.render_to_string(
        'SendCode/SendCode_temp.html',
        {
            'code': code
        }
    )
    send_mail('راستی آزمایی', ' ', EMAIL_HOST_USER, [email], fail_silently=True, html_message=html_message)


def errorBuild(massage):
    return Response({'detail': massage}, status=status.HTTP_400_BAD_REQUEST)
