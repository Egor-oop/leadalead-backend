from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .authentication import ExpiringTokenAuthentication

from django.conf import settings

import datetime
import pytz


class UserDetail(generics.RetrieveAPIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        print(self.request.user)
        return self.retrieve(request, *args, **kwargs)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        utc_now = datetime.datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        result = Token.objects.filter(
            user=user,
            created__lt=utc_now - settings.TOKEN_EXPIRE_TIME
        ).delete()

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })
