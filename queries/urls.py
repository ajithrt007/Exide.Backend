from django.urls import path
from .views import postMessage, getUnreadMessages, getReadMessages

urlpatterns =[
    path('postMessage/',postMessage,name='post_message'),
    path('getUnreadMessages/',getUnreadMessages,name='get_Unread_Messages'),
    path('getReadMessages/',getReadMessages,name='get_Read_Messages'),
]