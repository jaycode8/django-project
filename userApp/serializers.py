
from django.contrib.auth.models import User
from rest_framework import serializers

class UsersSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'email', 'password']
