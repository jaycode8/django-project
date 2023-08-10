from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework import response, status
from rest_framework.views import Response
from django.contrib.auth.models import User
from .serializers import UsersSerializer
from django.template import loader

from django.contrib.auth import authenticate, login, logout

# Create your views here.
@api_view(['POST'])
def test(req):
    usr = User.objects.filter(username = req.data['username'])
    if not usr:
        return Response({'msg':'user was not found.... Procceed to the signup page to be regestered'})
    found_usr = authenticate(username=req.data['username'], password=req.data['password'])
    if not found_usr:
        return Response({'msg':'password missmatch'})
    #if not found_usr.is_superuser:
    authed_user = User.objects.get(username=req.data['username'])
    user_data = {"username":authed_user.username, "email":authed_user.email, "password":authed_user.password}
    token, created = Token.objects.get_or_create(user= authed_user)
    login(req, authed_user)
    if not found_usr.is_superuser:
        return Response({'msg':'normal user authenticated','token':token.key, "user":user_data})
    return Response({'msg':'admin'})

@api_view(['GET'])
def log_template(req):
    template = loader.get_template('forms.html')
    return HttpResponse(template.render())

@api_view(['POST'])
def signup(req):
    serializer = UsersSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=req.data['username'])
        user.set_password(req.data['password'])
        user.save()
        print(serializer.data)
        return Response({"msg":"user saved successfuly", "user":serializer.data, 'status':status.HTTP_200_OK})
    return Response({"msg":"user not successfully saved", "error":serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})


@api_view(['POST'])
def signin(req):
    user = get_object_or_404(User, username=req.data['username'])
    if not user:
        return Response({'msg':'The user with that username doesnot exist', 'status':status.HTTP_400_BAD_REQUEST})
    if not user.check_password(req.data['password']):
        return Response({'msg':'password and username missmatch', 'status':status.HTTP_400_BAD_REQUEST})
    token, created = Token.objects.get_or_create(user=user)
    serializer = UsersSerializer(instance=user)
    return Response({"msg":"successfully loged in","token":token.key, "user":serializer.data, 'status':status.HTTP_200_OK})

@api_view(['GET'])
def logout_view(req):
    logout(req)
    return Response({'msg':'successfully logged out'})
