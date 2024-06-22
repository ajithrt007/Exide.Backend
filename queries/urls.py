from django.urls import path
from .views import postMessage, getUnreadMessages, getReadMessages, readUnreadMessage

urlpatterns =[
    path('postMessage/',postMessage,name='post_message'),
    path('readUnreadMessage/',readUnreadMessage,name='read_Unread_Message'),
    path('getUnreadMessages/',getUnreadMessages,name='get_Unread_Messages'),
    path('getReadMessages/',getReadMessages,name='get_Read_Messages'),
]