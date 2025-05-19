from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.db import IntegrityError



def login_view(request):
    return HttpResponse("Login") 


class RegisterUserView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'User registered successfully'}, status=status.HTTP_201_CREATED)
            return Response({'error':serializer.errors, 'success':False}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

