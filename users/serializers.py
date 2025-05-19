from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password', 'phone', 'email']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)
    
    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone must contain only digits.")
        return value
    



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid Login Credentials.')
        
        if not check_password(password, user.password):
            raise serializers.ValidationError('Password is incorrect')
        
        refresh = RefreshToken.for_user(user)
        return {
            "access_token":str(refresh.access_token),
            "refresh":str(refresh),
            "user_id":user.id,
            "username":user.username
        }