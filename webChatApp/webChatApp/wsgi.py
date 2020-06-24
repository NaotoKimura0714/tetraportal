import os
from django.core.wsgi import get_wsgi_application
from app.logUtil import logUtil
import datetime

# 保存するファイル名を指定
log_folder = '{0}.log'.format(datetime.date.today())
# ログの初期設定を行う
logger = logUtil.setup_logger(log_folder)

# ログを出力
logger.info("WSGI Start")

import sys
#sys.path.append('/home/user001/webChatApp/env/Lib/site-packages')
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

FILE_PATH = os.path.dirname(__file__)
PROJECT_NAME = os.path.basename(FILE_PATH)

sys.path.append(os.path.dirname(FILE_PATH))
sys.path.append(FILE_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", PROJECT_NAME + ".settings")

#os.environ.setdefault(
#'DJANGO_SETTINGS_MODULE',
#'webChatApp.settings')

logger.debug("WSGI middle")
# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()

logger.info("WSGI end")
