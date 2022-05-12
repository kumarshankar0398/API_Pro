import string
from random import *
from django.core.mail import send_mail
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import User
from .serializer import UserSerializer, UserLoginSerializer, UserLogoutSerializer, ResetPasswordSErializer, \
    ResetPassSerializer
from APIProject import settings


class Record(generics.ListCreateAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(generics.GenericAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


def index(request):
    return redirect('/api/login')


ran = ''
email = ''


class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSErializer
    model = User

    def post(self, request):
        global ran, email
        if User.objects.filter(email=request.POST['email']):
            email = request.POST['email']
            subject = "Sending an email with Django"
            S = 8
            ran = ''.join(choices(string.ascii_letters + string.digits, k=S))
            message = str(ran)
            # send the email to the recipent
            send_mail(subject, message,
                      settings.DEFAULT_FROM_EMAIL, ['kumar.shankar0797@gmail.com'])
            return Response(
                {'msg': 'Please check your email', 'link for resetting password': 'http://127.0.0.1:8000/resetpwd/'})
        else:
            return Response({'msg': 'this email is not registered with us'})


class ResetYourPassword(generics.GenericAPIView):
    serializer_class = ResetPassSerializer
    model = User

    def post(self, request):
        if request.POST['received_code'] == ran and request.POST['password'] == request.POST['confirm_password']:
            print(request.POST['received_code'])
            print(ran)
            print("Under resetpass")
            u = User.objects.get(email=email)
            print(u.email)
            u.set_password(request.POST['password'])
            print("Password setted")
            u.save()
            return Response({'msg': 'Password has been reset. You can login now with your new password',
                             'login here': 'http://127.0.0.1:8000/login/'})

        return Response({'msg': 'Please enter valid code and password and confirm password should match.'})
