"""
Definition of urls for webChatApp.
"""

from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import views
from account import views
from django.conf.urls.static import static
from django.conf import settings
from app.logUtil import logUtil
import datetime

# 保存するファイル名を指定
log_folder = '{0}.log'.format(datetime.date.today())
# ログの初期設定を行う
logger = logUtil.setup_logger(log_folder)

 # ログを出力
logger.debug("webChatApp - start urls")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('app.urls')),
    path('', include('account.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

 # ログを出力
logger.debug("webChatApp - end urls")
