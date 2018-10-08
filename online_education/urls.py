"""online_education URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
import xadmin
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ForgetPwdView, LogOutView
from users.views import ActiveUserView, ResetView, ModifyPwdView, IndexView
from django.views.static import serve
from online_education.settings import MEDIA_ROOT #, #STATIC_ROOT


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name="index"),  # TemplateView.as_view(template_name="index.html")
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogOutView.as_view(), name="logout"),
    url(r'register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构url
    url(r'^org/', include('organization.urls'), name="org"),
    # 课程相关url
    url(r'^course/', include('courses.urls'), name="course"),
    # 用户相关url
    url(r'^users/', include('users.urls'), name="users"),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 静态文件的查找debug为false的时候
   # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    # 富文本相关url
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]

# 全局404
handler404 = 'users.views.page_not_found'
# 全局500
handler500 = 'users.views.page_error'

