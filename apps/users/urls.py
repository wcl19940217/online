from django.conf.urls import url
from .views import UsersInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView
from .views import MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView


urlpatterns = [
    # 用户信息
    url(r'^info/$', UsersInfoView.as_view(), name="users_info"),
    # 用户头像修改
    url(r'^image/upload/$', UploadImageView.as_view(), name="user_image_upload"),
    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="user_update_pwd"),
    # 邮箱发送验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="user_update_pwd"),
    # 更改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name="user_mycourse"),
    # 我收藏的课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),
    # 我收藏的讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    # 我收藏的课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),
    # 我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name="mymessage"),

]
