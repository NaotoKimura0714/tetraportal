from django.urls import path
from account import views
from app.logUtil import logUtil
import datetime

# 保存するファイル名を指定
log_folder = '{0}.log'.format(datetime.date.today())
# ログの初期設定を行う
logger = logUtil.setup_logger(log_folder)

 # ログを出力
logger.debug("accounts - start urls")
app_name ='accounts'

urlpatterns =[
    path('', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
]
 # ログを出力
logger.debug("accounts - end urls")