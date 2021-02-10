from django.shortcuts import render
from rest_framework import generics, status, views
from rest_framework.response import Response
from .serializers import RegisterSerializer, EmailVerification
from django.contrib.auth import get_user_model
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
User = get_user_model()


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        """"Get data via post and then push it to the serializer to handle for validation and save """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.errors
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('authentication:email-verify')
        absolute_url = 'http://' + current_site + \
            relativeLink + '?token=' + str(token)
        email_body = 'Hi' + user.username + \
            'Use the link below to verify your email \n' + absolute_url
        data = {
            'email_body': email_body,
            'email_subject': 'Verify Your Email',
            'to_email': user.email,
        }
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerification
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


# use payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])  instead of  payload = jwt.decode(token, settings.SECRET_KEY).
# JWT decoding required algorithm passed as a parameter
