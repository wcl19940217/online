from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord, Banner
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyForm, UploadImageForm, UserInfoForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
import json
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class CustomBackend(ModelBackend):
    """
    支持邮箱和密码登录
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username)|Q(password=password))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    """
    登录
    """
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('index'))  # django提供的重定向方法
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogOutView(View):
    """
    登录退出
    """
    def get(self, request):
        logout(request)   # django提供的退出方法
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index')) # django提供的重定向方法


class RegisterView(View):
    """
    注册
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": '用户已存在'})
            pass_word = request.POST.get("password", '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 写入注册消息
            user_message = UserMessage()
            user_message.user = user_profile
            user_message.message = "欢迎注册"
            user_message.save()

            send_register_email(user_name, 'register')
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveUserView(View):
    """
    认证
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "404.html")
        return render(request, "login.html")


class ForgetPwdView(View):
    """
    忘记密码
    """
    def get(self, request):
        forget_form = ForgetForm(request.POST)
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", '')
            send_register_email(email, 'forget')
            return render(request, 'send_sussful.html')
        else:
            return render(request, '404.html')


class ResetView(View):
    """
    重置密码
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})

        else:
            return render(request, "404.html")

    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwds1 = request.POST.get('password', '')
            pwds2 = request.POST.get('password1', '')
            email = request.POST.get('email', '')
            if pwds1 != pwds2:
                return render(request, 'password_reset.html', {"email": email, "msg": "密码不一致"})

            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwds2)
            user.save()
            return render(request, 'login.html')

        else:
            email = request.POST.get('email', '')
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class ModifyPwdView(View):
    """
    密码修改
    """
    def post(self, request):
        pwds1 = request.POST.get('password1', '')
        pwds2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        if pwds1 != pwds2:
            return render(request, 'password_reset.html', {"email": email, "msg": "密码不一致"})
        else:
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwds2)
            user.save()
            return render(request, 'login.html')


class UsersInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        current_page = "info"
        return render(request, 'usercenter-info.html', {
            'current_page': current_page
        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        # user = request.user
        # nick_name = request.POST.get('nick_name', '')
        # gender = request.POST.get('gender', '')
        # birthday = request.POST.get('birthday', '')
        # address = request.POST.get('address', '')
        # mobile = request.POST.get('mobile', '')
        # print(user, nick_name, gender, birthday, address, mobile)
        #
        # users = UserProfile.objects.filter(username=user)
        # print(users, 88888888888888888888)
        # users.nick_name = nick_name
        # users.gender = gender
        # users.birthday = birthday
        # users.address = address
        # users.mobile = mobile
        # try:
        #     users.save()
        #     return HttpResponse('{"status":"success"}', content_type='application/json')
        # except Exception as e:
        #     return HttpResponse(json.dumps(e), content_type='application/json')
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"修改失败"}', content_type='application/json')
        # 第二种实现
        # image_form = UploadImageForm(request.POST, request.FILES)
        # if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()


class UpdatePwdView(View):
    """
    用户中心密码修改
    """
    def post(self, request):
        pwds1 = request.POST.get('password1', '')
        pwds2 = request.POST.get('password2', '')
        if pwds1 != pwds2:
            return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
        else:
            user = request.user
            user.password = make_password(pwds2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已存在"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status": "success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')

        else:
            return HttpResponse('{"email": "验证码错误"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self, request):
        current_page = "mycourse"
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
            'current_page': current_page
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我的收藏机构
    """
    def get(self, request):
        current_page = "myfav"
        org_list = []
        user_myfav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in user_myfav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
            'current_page': current_page,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我的收藏讲师
    """
    def get(self, request):
        current_page = "myfav"
        teacher_list = []
        user_myfav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in user_myfav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
            'current_page': current_page,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我的收藏课程
    """
    def get(self, request):
        current_page = "myfav"
        course_list = []
        user_myfav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in user_myfav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
            'current_page': current_page,
        })


class MyMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        current_page = 'myssage'
        all_message = UserMessage.objects.filter(user=request.user.id)
        # 用户进入消息后，清空已读消息
        all_unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 1, request=request)

        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'current_page': current_page,
            'messages': messages
        })


class IndexView(View):
    """
    首页
    """
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=False)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs

        })


# 404页面
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 500页面
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

