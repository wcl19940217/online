from users.models import EmailVerifyRecord
import random
from django.core.mail import send_mail
from online_education.settings import EMAIL_FROM


def random_str(randomlength=8):
    strs = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwSsYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        strs += chars[random.randint(0, length)]
    return strs


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = "注册激活链接"
        email_body = "请点击下面的链接激活账号：http://127.0.0.1:8000/active/{}".format(code)
        email_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if email_status:
            pass

    if send_type == 'forget':
        email_title = "密码找回"
        email_body = "请点击下面的链接重置密码：http://127.0.0.1:8000/reset/{}".format(code)
        email_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if email_status:
            pass

    if send_type == 'update_email':
        email_title = "邮箱修改"
        email_body = "你的邮箱验证码为{0}".format(code)
        email_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if email_status:
            pass






