
#from django.conf.urls import url
from django.urls import path
 
from . import consumers
 
websocket_urlpatterns = [
#    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    path('ws/chat/rooms/<str:room_name>/<int:room_id>/<str:user_name>/', consumers.ChatConsumer),
]