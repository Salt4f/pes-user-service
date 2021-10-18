from rest_framework import serializers
from snippets.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email','password', 'nickName','token']