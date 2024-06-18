from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import AccessToken

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_password(request):
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    decoded_token = AccessToken(token)
    user_id = decoded_token.payload.get('user_id')
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not request.user.is_superuser:
        return Response({'error': 'Only superusers can update passwords'}, status=status.HTTP_403_FORBIDDEN)

    if not new_password:
        return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
        if not user.is_superuser:
            return Response({'error': 'User is not a superuser'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    
        user.password = make_password(new_password)
        user.save()

        return Response({'success': 'Password updated successfully'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)