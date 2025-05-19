from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserLoginSerializer
from django.db import IntegrityError
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message':'User registered successfully'}, status=status.HTTP_201_CREATED)
            return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LoginUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print(request)
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)