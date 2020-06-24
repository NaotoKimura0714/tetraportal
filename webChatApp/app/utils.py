import base64
#import pyotp
import qrcode
from io import BytesIO



def get_secret(user):
    """
    本当は秘密鍵を設定するんだろうけど、面倒なので、「メールアドレス」と「登録日時」をくっつけたモノを使う。一意になればとりあえずいいかなと。。。
    """
    return base64.b32encode(
        (user.email + str(user.date_joined)).encode()
    ).decode()


def get_auth_url(email, secret, issuer='ProjectName'):
    """
    下に書いてあるURLフォーマットで設定する必要がある。
    最初の「isr」「uid」は、Google認証システムのアプリ上にも表示されるから、プロジェクト名とメールアドレスを突っ込むのが無難だと思う。
    """
    url_template = 'otpauth://totp/{isr}:{uid}?secret={secret}&issuer={isr}'
    return url_template.format(
        uid=email,
        secret=secret,
        isr="TSD_PORTAL")


def get_image_b64(url):
    qr = qrcode.make(url)
    img = BytesIO()
    qr.save(img)
    return base64.b64encode(img.getvalue()).decode()


#def make_onetime_pass(user):
#
#    secret_key = base64.b32encode((user.email).encode()).decode("UTF-8")
#    totp = pyotp.TOTP(secret_key)
#
#    print(totp.now())
#
#    return totp.now()

#def check_onetime_pass(one_time_pass, input_pass):
#
#    if(one_time_pass == input_pass):
#        return True
#    else:
#        return False

     
#def make_qrcode(onetime_pass):
#
#    img = BytesIO()
#    qr = qrcode.make(onetime_pass)
#    qr.save(img)
#
#    return  base64.b64encode(img.getvalue()).decode()