from rest_framework.serializers import Serializer, ModelSerializer, CharField, ValidationError
from rest_framework.fields import CharField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.users.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
   @classmethod
   def get_token(cls, user):
      token = super().get_token(user)

      # Add custom claims
      token['role'] = user.role

      return token


class UserCustomSerializer(ModelSerializer):
   class Meta:
      model = User
      fields = ('id','email', 'name', 'photo', 'role')


class UserSerializer(ModelSerializer):
   class Meta:
      model = User
      fields = '__all__'

   def create(self, validated_data):
      user = User(**validated_data)
      user.set_password(validated_data['password'])
      user.save()
      return user
   
   def to_representation(self, instance):
      return {
         'id': instance.id,
         'email': instance.email,
         'name': instance.name,
         'photo': instance.photo.url,
         'role': instance.role,
      }


class UserUpdateSerializer(ModelSerializer):
   class Meta:
      model = User
      fields = ('email', 'name')


class PasswordSerializer(Serializer):
   password = CharField(max_length=128, min_length=6, write_only=True)
   password2 = CharField(max_length=128, min_length=6, write_only=True)

   def validate(self, data):
      if data['password'] != data['password2']:
         raise ValidationError(
            { 'password': 'La contraseña no son iguales' }
         )
      return data
