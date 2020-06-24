from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import(LoginView, LogoutView)
from .forms import LoginForm

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import dumps
from django.core.signing import BadSignature, SignatureExpired, loads
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.template.loader import get_template
from django.views import generic
from .forms import CustomUserCreateForm
from . import utils
import requests
from app.logUtil import logUtil
import datetime

User = get_user_model()

# 保存するファイル名を指定
log_folder = '{0}.log'.format(datetime.date.today())
# ログの初期設定を行う
logger = logUtil.setup_logger(log_folder)


class Login(LoginView):

    # ログを出力
    logger.debug("ログイン画面の表示処理開始")
    """ログインページ"""
    form_class = LoginForm
    template_name = 'app/login.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/chat/top/')
        return super().get(request, **kwargs)

    def form_valid(self, form):
        captcha = self.request.POST.get("g-recaptcha-response")
        if captcha:
            auth_url = 'https://www.google.com/recaptcha/api/siteverify?secret={}&response={}'
            auth_url = auth_url.format('6Ld2MfQUAAAAAGtGe4zI_r-xaOLpuEkD4vTyt7vq', captcha)
            response = requests.get(auth_url)
            if response.json().get('success'):
                return super().form_valid(form)
 
        # ビューからフォームにエラーを追加できます。第一引数がNoneの場合は、{{ form.non_field_errors }}で表示される
        form.add_error(None, 'ロボットではないチェックを入れてください')  # キーが間違っている場合もあるが、一緒のエラー内容にしちゃってます。
        return self.form_invalid(form)


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'app/login.html'

class UserCreate(generic.CreateView):
    """ユーザ登録"""
    template_name = 'app/user_create.html'
    form_class = CustomUserCreateForm

    def get(self, request, **kwargs):
        #if request.user.is_authenticated:
        #    return HttpResponseRedirect('/chat/top/')
        return super().get(request, **kwargs)

    def form_valid(self, form):
        # 仮登録
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # メール送信
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user
        }
        subject_template = get_template('app/mail/subject.txt')
        message_template = get_template('app/mail/message.txt')
        subject = subject_template.render(context)
        message = message_template.render(context)
        user.email_user(subject, message)
        print(message)   
        return redirect('accounts:user_create')


class UserCreateComplete(generic.TemplateView):
    """本登録完了"""
    template_name = 'app/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        if request.user.is_authenticated:
            return HttpResponseRedirect('/chat/top/')

        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoenNotExist:
            return HttpResponseBadRequest()

        if not user.is_active:
            # 問題なければ本登録とする
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()

            # QRコード生成
            request.session["img"] = utils.get_image_b64(utils.get_auth_url(user.email, utils.get_secret(user)))

            return super().get(request, **kwargs)

        return HttpResponseBadRequest()

