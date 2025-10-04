from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from core.models import UserProfile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.get_username(),
        'email': getattr(user, 'email', ''),
        'is_authenticated': user.is_authenticated,
    })


@api_view(['POST'])
@permission_classes([])
def register(request):
    data = request.data or {}
    email = (data.get('email') or '').strip()
    password = (data.get('password') or '').strip()
    # We align username with email so the existing login form works
    username = (data.get('username') or '').strip() or email
    first_name = (data.get('first_name') or '').strip()
    last_name = (data.get('last_name') or '').strip()

    if not email or not password:
        return Response({'detail': 'email and password required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'detail': 'email already registered'}, status=status.HTTP_400_BAD_REQUEST)
    if not username:
        return Response({'detail': 'username required'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'detail': 'username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    user = User(username=username, email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.save()

    # Create associated profile with basic fields mirrored from user
    UserProfile.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )

    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }, status=status.HTTP_201_CREATED)




