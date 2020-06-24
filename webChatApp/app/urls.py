
#from django.conf.urls import url
from django.urls import path
 
from .views import *
from app.logUtil import logUtil
import datetime

# 保存するファイル名を指定
log_folder = '{0}.log'.format(datetime.date.today())
# ログの初期設定を行う
logger = logUtil.setup_logger(log_folder)

 # ログを出力
logger.debug("chat - start urls")
app_name ='chat'
 
urlpatterns = [
#    url(r'^$', rooms, name='rooms'),
#    url(r'^(?P<room_name>[^/]+)/$', make_room, name='make_room'),
#    url(r'^(?P<room_name>[^/]+)/^(?P<room_id>[0-9]+)/$', room, name='room'),

    path('rooms/', rooms, name='rooms'),
    path('top/', top, name='top'),
    path('rooms/<str:room_name>/', make_room, name='make_room'),
    path('rooms/<str:room_name>/<int:room_id>/', room, name='room'),
    path('delete_room/<int:room_id>/', delete_room, name='delete_room'),
    path('todo_list/',todo_list,name='todo_list'),
    path('new_todo/',new_todo,name='new_todo'),
    path('delete/<list_id>', delete, name="delete"),
    path('complete/<list_id>', complete, name="complete"),
    path('todo_wbs/', todo_wbs, name="todo_wbs"),
]
 # ログを出力
logger.debug("chat - end urls")
