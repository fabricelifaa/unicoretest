from django.contrib.auth.models import User
from rest_framework import serializers
# from unicoretest.models import Tokens, Restaurants, Users
from unicoretest.models import Tokens, Restaurants


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        # For User 
        # model = Users
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tokens
        fields = ['token', 'public_key', 'created_date', 'user_id']

class RestaurantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = ['name', 'lng', 'lat', 'desc', 'adress']