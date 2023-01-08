# Django
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

# RestFramework
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAdminUser

# Jwt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

# Users
from apps.users.models import User
from apps.users.serializer import (
   UserSerializer, UserUpdateSerializer, UserCustomSerializer, CustomTokenObtainPairSerializer, PasswordSerializer
)

class UserViewSet(GenericViewSet):
   model = User
   serializer_class = UserSerializer
   update_serializer_class = UserUpdateSerializer
   password_serializer_class = PasswordSerializer
   queryset = None

   def get_object(self, pk):
      return get_object_or_404(self.model, pk=pk)

   def get_queryset(self):
      if self.queryset is None:
         self.queryset = self.model.objects.all()
      return self.queryset

   def list(self, request):
      users = self.get_queryset()
      users_selializer = self.serializer_class(users, many=True)
      data = {
         'msg': 'OK',
         'data': users_selializer.data
      }
      return Response(data)

   def retrieve(self, reques, pk):
      user = self.get_object(pk)
      user_serializer = self.serializer_class(user)
      data = {
         'msg': 'OK',
         'data': user_serializer.data
      }
      return Response(data, status=HTTP_200_OK)

   @action(detail=True, methods=['post'])
   def password(self, request, pk=None):
      user = self.get_object(pk)
      password_serializer = self.password_serializer_class(data=request.data)
      if password_serializer.is_valid():
         user.set_password(password_serializer.validated_data['password'])
         user.save()
         return Response({
            'message': 'Contraseña actualizada correctamente'
         })
      return Response({
         'message': 'Hay errores en la información enviada',
         'errors': password_serializer.errors
      }, status=HTTP_400_BAD_REQUEST)
   
   def create(self, request):
      user_serializer = self.serializer_class(data=request.data)
      if user_serializer.is_valid():
         user_serializer.save()
         data = {
            'status': 201,
            'message': 'Usuario creado correctamente',
            'data': user_serializer.data
         }
         return Response(data, HTTP_201_CREATED)
      data = {
         'status': 400,
         'message': 'Se produjo un error al crear el Usuario',
         'data': None
      }
      return Response(data, HTTP_400_BAD_REQUEST)

   def update(self, request, pk):
      user = self.get_object(pk)
      user_serializer = self.update_serializer_class(user, data=request.data)
      if user_serializer.is_valid():
         user_serializer.save()
         return Response({
            'status': 200,
            'message': 'Usuario actualizado correctamente',
            'data': user_serializer.data
         }, status=HTTP_200_OK)
      
      return Response({
         'status': 400,
         'message': 'Se produjo un error al actualizar los datos',
         'data': None
      }, status=HTTP_400_BAD_REQUEST)
   
   def destroy(self, request, pk):
      user_destroy = self.model.objects.filter(id=pk).update(status='eliminated')
      if user_destroy == 1:
         return Response({
            'message': 'Usuario eliminado correctamente'
         })
      return Response({
         'message': 'No existe el usuario que desea eliminar'
      }, status=HTTP_404_NOT_FOUND)


class Login(TokenObtainPairView):
   serializer_class = CustomTokenObtainPairSerializer

   def post(self, request, *args, **kwargs):
      email = request.data.get('email', '')
      password = request.data.get('password', '')
      user = authenticate(
         email=email,
         password=password
      )

      if user:
         login_serializer = self.serializer_class(data=request.data)
         if login_serializer.is_valid():
            user_serializer = UserCustomSerializer(user)
            data = {
               'status': 201,
               'message': 'Inicio de Sesion Existoso',
               'data': {
                  'token': login_serializer.validated_data.get('access'),
                  'refresh': login_serializer.validated_data.get('refresh'),
                  **user_serializer.data,
               }
            }
            return Response(data, status=HTTP_201_CREATED)
         return Response({ 'error': 'Correo o contraseña incorrectos' }, status=HTTP_400_BAD_REQUEST)
      return Response({ 'error': 'Correo o contraseña incorrectos' }, status=HTTP_400_BAD_REQUEST)


class Logout(GenericAPIView):
   def post(self, request, *args, **kwargs):
      user = User.objects.filter(id=request.data.get('user', 0))
      if user.exists():
         RefreshToken.for_user(user.first())
         return Response({ 'message': 'Sesión cerrada correctamente.' }, status=HTTP_200_OK)
      return Response({ 'error': 'No existe este usuario.' }, status=HTTP_400_BAD_REQUEST)