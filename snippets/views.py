from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from drf_yasg import openapi
from snippets.models import User
from snippets.serializers import UserSerializer
from rest_framework import generics
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework_api_key.crypto import KeyGenerator
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
import json


#
#class UserVerification(generics.ListCreateAPIView):
# 
#    serializer_class = UserSerializer
#    
#    def get_queryset(self):
#        id = self.request.POST.get('id')
#        token = self.request.POST.get('token')
#        
#        queryset = User.objects.filter(id = id).filter(token = token)
#        
#        #if we have a user that match the id and the token then it returns all the data from the user
#        #Otherwise it returns an empty JSON
#        return queryset
#
keyGenerator = KeyGenerator(prefix_length=2, secret_key_length=32)



@swagger_auto_schema(methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id', 'token'],
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'token': openapi.Schema(type=openapi.TYPE_STRING)
        },
    )
)
@api_view(['POST'])
def user_verification(request, pk=None):
    user = request.data
    user_serializer = UserSerializer(data = user)
    if(User.objects.filter(id = user['id']).filter(token = user['token']).exists()):
        user_serializer = UserSerializer(user)
        return Response({ 'verification':True}, status = status.HTTP_201_CREATED)
    return Response({'verification':False}, status = status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password', 'nickName'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'nickName': openapi.Schema(type=openapi.TYPE_STRING)
        },
    ),
    responses={"201": openapi.Response(
        description="custom 201 description",
        
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'token': openapi.Schema(type=openapi.TYPE_STRING),
        },
        examples={
            "application/json": {
                "id": "1",
                "token": "4y1729bsdq318",
            }
        }
    )}
)
@api_view(['GET','POST'])
def all_users_api_view(request,pk=None):

    if request.method == 'GET':
        user = User.objects.all()
        user_serializer = UserSerializer(user, many = True)
        return Response(user_serializer.data, status = status.HTTP_200_OK)

    if request.method == 'POST':
        user = request.data
        user_serializer = UserSerializer(data = user)
        if user_serializer.is_valid():
            user_serializer.save(token=keyGenerator.get_secret_key())
            return Response({ 'id': user_serializer.data.get('id'), 'token': user_serializer.data.get('token')}, status = status.HTTP_201_CREATED)
        return Response(user_serializer.errors)


@swagger_auto_schema(methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING)
        },
    )
)
@api_view(['POST'])
def user_login(request, pk=None):
    user = request.data
    print(request.data) 
    user_serializer = UserSerializer(data = user)
    if user_serializer.is_valid():
        if(User.objects.filter(email = user['email']).filter(password = user['password']).exists()):
            user = User.objects.filter(email = user['email']).first()
            user_serializer = UserSerializer(user)
            return Response({ 'id': user_serializer.data.get('id'), 'token': user_serializer.data.get('token')}, status = status.HTTP_201_CREATED)
    return Response(user_serializer.errors)


@swagger_auto_schema(methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id', 'token'],
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'token': openapi.Schema(type=openapi.TYPE_STRING)
        },
    )
)
@api_view(['POST'])
def user_login_id_token(request, pk=None):
    user = request.data 
    user_serializer = UserSerializer(data = user)
    if(User.objects.filter(id = user['id']).filter(token = user['token']).exists()):
        user = User.objects.filter(id = user['id']).first()
        user_serializer = UserSerializer(user)
        return Response({ 'id': user_serializer.data.get('id'), 'token': user_serializer.data.get('token')}, status = status.HTTP_201_CREATED)
    return Response(status = status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def user_detail_api_view(request, pk=None):

    if request.method == 'GET':
        user = User.objects.filter(id = pk).first()
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status = status.HTTP_201_CREATED)




@swagger_auto_schema(methods=['put'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password', 'passwordNew', 'token'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'passwordNew': openapi.Schema(type=openapi.TYPE_STRING),
            'token': openapi.Schema(type=openapi.TYPE_STRING)
        },
    )
)
@api_view(['PUT'])
def user_change_pass_api_view(request, pk=None):

    user = User.objects.filter(id = pk).first()
    user_serializer = UserSerializer(user,data = request.data)
    
    if user_serializer.is_valid():
        if(User.objects.filter(email =request.data['email'] ).filter(password= request.data['password']).exists()):
            user_serializer.save(password = request.data['passwordNew'],token=keyGenerator.get_secret_key())
            return Response(user_serializer.data)
    return Response(user_serializer.errors)
    

@swagger_auto_schema(methods=['put'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password', 'passwordNew', 'token'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'passwordNew': openapi.Schema(type=openapi.TYPE_STRING),
            'token': openapi.Schema(type=openapi.TYPE_STRING)
        },
    )
)
@api_view(['PUT'])
def user_change_pass_api_view(request, pk=None):

    user = User.objects.filter(id = pk).first()
    user_serializer = UserSerializer(user,data = request.data)
    
    if user_serializer.is_valid():
        if(User.objects.filter(email =request.data['email'] ).filter(password= request.data['password']).exists()):
            user_serializer.save(password = request.data['passwordNew'],token=keyGenerator.get_secret_key())
            return Response(user_serializer.data)
    return Response(user_serializer.errors)


@swagger_auto_schema(methods=['put'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id', 'password', 'token'],
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'token': openapi.Schema(type=openapi.TYPE_STRING)
        },
    )
)
@api_view(['PUT'])
def user_change_pass_id_api_view(request, pk=None):

    user = User.objects.filter(id = pk).first()
    user_serializer = UserSerializer(user,data = request.data)
    
    if user_serializer.is_valid():
        if(User.objects.filter(id =request.data['id'] ).filter(token= request.data['token']).exists()):
            user_serializer.save(password = request.data['password'], token=keyGenerator.get_secret_key())
            return Response(user_serializer.data, status = status.HTTP_201_CREATED)
    return Response(status= status.HTTP_404_NOT_FOUND)
