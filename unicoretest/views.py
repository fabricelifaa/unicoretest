from django.shortcuts import render
# Usefull modules
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from unicoretest.models import Tokens, Restaurants
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from unicoretest.serializers import UserSerializer, TokenSerializer, RestaurantsSerializer
from rest_framework.decorators import api_view
from datetime import date
from unicoretest.utils import keys_generator

# Create your views here.


@api_view(['POST'])
def Register_user(request):
    """
    API endpoint that use to register new user.
    """
    user_data = JSONParser().parse(request)
    user_serializer = UserSerializer(data=user_data)

    if user_serializer.is_valid():
        user_serializer.save()
        # set password
        u = User.objects.get(username=user_data['username'])
        u.set_password(user_data['password'])
        u.save()
        return JsonResponse(
            {
                'message':
                'User ' + user_data['username'] +
                ' is registered successfylly.'
            },
            status=status.HTTP_201_CREATED)
    else:
        # return JsonResponse({'message': 'Bad request please check your request and try agin!'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(user_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def Login(request):
    """
    API endpoint that use to logging user.
    """
    if request.method == 'GET':
        return JsonResponse(
            {'message': 'You are not connected please logged in and try again!'},
            status=status.HTTP_400_BAD_REQUEST)


    user_connected = request.user.id
    if user_connected is not None:
        return JsonResponse(
            {'message': 'User is already connected use api_keys endpoints for get your keys!'},
            status=status.HTTP_400_BAD_REQUEST)
    
    user_credential = JSONParser().parse(request)
    
    if (not 'username' in user_credential) or (not 'password' in user_credential):
        return JsonResponse(
            {'message': 'Bad request please check your request and try agin!'},
            status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=user_credential['username'],
                        password=user_credential['password'])

    if user is not None:

        login(request, user)

        today = date.today()
        secret_key = keys_generator(size=27)
        public_key = keys_generator()
        Token_Serializer = TokenSerializer(
            data={
                "token": secret_key,
                "public_key": public_key,
                "ceated_date": today.strftime("%Y-%m-%d"),
                "user_id": user.id
            })
        
        if Token_Serializer.is_valid():
            Token_Serializer.save()

        else:
            return JsonResponse(
                Token_Serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        

        return JsonResponse(
            {
                'public_key': public_key,
                'secret_key': secret_key
            },
            status=status.HTTP_201_CREATED)

    else:
        return JsonResponse(
            {'message': 'User not exist. Check your fields and try again!'},
            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Logout(request):
    """
    API endpoint that use to logged out user.
    """
    logout(request)
    return JsonResponse({'message': 'User is logged out successfylly.'},
                        status=status.HTTP_201_CREATED)


@api_view(['GET'])
@login_required(login_url='/unicore/login/')
def Get_keys(request):
    """
    API endpoint that use to get user keys.
    """
    user = request.user.id
    if user is None:
        return JsonResponse(
            {'message': 'Bad request please check your request and try agin!'},
            status=status.HTTP_400_BAD_REQUEST)

    user_tokens = Tokens.objects.filter(user_id = user).order_by('id').reverse()[0]
    token_seria = TokenSerializer(user_tokens)
    if user_tokens is not None:
        return JsonResponse(
            {
                'public_key': token_seria.data['public_key'],
                'secret_key': token_seria.data['token']
            },
            status=status.HTTP_201_CREATED)
    else:

        return JsonResponse(
            {'message': 'Bad request please check your request and try agin!'},
            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Get_restaurants(request):
    """
    API endpoint that use to get restaurant.
    """
    if not 'X-Public-Key' in request.headers and not 'X-Secret-Key' in  request.headers:
        return JsonResponse(
            {'message': 'Permission denied. Check your request and try again.'},
            status=status.HTTP_400_BAD_REQUEST)

    geo_data = JSONParser().parse(request)
    if not 'lat' in geo_data and not 'lng' in geo_data:
        return JsonResponse(
            {'message': 'Bad request please check your fields and try agin!'},
            status=status.HTTP_400_BAD_REQUEST)

    lat = geo_data['lat']
    lng = geo_data['lng']
    public_key = request.headers['X-Public-Key']
    secret_key = request.headers['X-Secret-Key']

    check_tokens = Tokens.objects.filter(public_key = public_key, token= secret_key).order_by('id').reverse()[0]

    if check_tokens is not None:
        # review request and integrate get around in 3km radius restaurant
        restaurant_lists = Restaurants.objects.extra(where=['lat >= %s', 'lng <= %s'], params=[lat, lng])

        if restaurant_lists is not None:
            serialize_lists = RestaurantsSerializer(restaurant_lists, many=True)
            return JsonResponse(
                serialize_lists.data,
                status=status.HTTP_201_CREATED)
        
        else:
            return JsonResponse(
                {'message': 'Restaurant not found for your localisation'},
                status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(
            {'message': 'Permission denied. Check your request and try again.'},
            status=status.HTTP_400_BAD_REQUEST)
    
