from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuerySerializer
import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Query
from .decorators import limit_post_submissions

@api_view(['POST'])
@limit_post_submissions(rate_limit=5, time_window=3600)
def postMessage(request):
    name=request.data.get('name')
    email=request.data.get('email')
    phno=request.data.get('phno')
    subject=request.data.get('subject')
    message=request.data.get('message','')

    data={
        "name": name,
        "email": email,
        "ph_no": phno,
        "subject": subject,
        "msg": message,
        "timestamp": datetime.datetime.now(),
        "answered": False
    }

    query_serializer=QuerySerializer(data=data)
    if not query_serializer.is_valid():
        return Response("Something Wrong",query_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    query_serializer.save()
    return Response({'message': 'Message posted successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def readUnreadMessage(request):
    msg_id=request.data.get('id')

    if not msg_id:
        return Response({'error': 'Message ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        message = Query.objects.get(id=msg_id)
    except Query.DoesNotExist:
        return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    message.answered = True
    message.save()

    return Response({'message': 'Message status updated to answered'}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUnreadMessages(request):
    unread_messages=list(Query.objects.filter(answered=False))
    serializer=QuerySerializer(unread_messages,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getReadMessages(request):
    read_messages=list(Query.objects.filter(answered=True))
    serializer=QuerySerializer(read_messages,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)