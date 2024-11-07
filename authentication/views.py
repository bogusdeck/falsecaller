from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, AuthenticationFailed

User = get_user_model()

def index(request):
    return redirect('login')

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    try:
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "User created successfully", 
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)
    except ValidationError as e:
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    try:
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            user = authenticate(phone_number=phone_number, password=password)
            
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "message": "Login successful", 
                    "token": token.key
                }, status=status.HTTP_200_OK)
            raise AuthenticationFailed("Invalid credentials")
        
        raise ValidationError(serializer.errors)
    except AuthenticationFailed as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    except ValidationError as e:
        return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)