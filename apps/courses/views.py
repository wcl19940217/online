from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
from .models import Course, CoursesResource, Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, CourseComments, UserCourse
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')

        search_keywords = request.GET.get('keywords', '')
        # 课程搜索
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(
                detail__icontains=search_keywords))

        sort = request.GET.get('sort', '')
        # 筛选排序
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "courses":
                all_courses = all_courses.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses

        })


class CourseDetailView(View):
    """
    课程详情
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)
        else:
            relate_course = []

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_course': relate_course,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)

        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_coursers = UserCourse.objects.filter(course=course)
        user_ids = [user_courser.user.id for user_courser in user_coursers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出课程id
        course_ids = [user_courser.course.id for user_courser in user_coursers]
        # 获取学过该课程的其他用户的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")

        all_resources = CoursesResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses
        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程留言信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)

        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_coursers = UserCourse.objects.filter(course=course)
        user_ids = [user_courser.user.id for user_courser in user_coursers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出课程id
        course_ids = [user_courser.course.id for user_courser in user_coursers]
        # 获取学过该课程的其他用户的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")

        all_resources = CoursesResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comments': all_comments,
            'relate_courses': relate_courses
        })


class AddCommentsView(View):
    """
    用户添加评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', '')
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"评论失败"}', content_type='application/json')


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()
        # 查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)

        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_coursers = UserCourse.objects.filter(course=course)
        user_ids = [user_courser.user.id for user_courser in user_coursers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出课程id
        course_ids = [user_courser.course.id for user_courser in user_coursers]
        # 获取学过该课程的其他用户的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")
        all_resources = CoursesResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return render(request, 'course-play.html', {
            'course': course,
            'relate_courses': relate_courses,
            'all_resources': all_resources,
            'all_comments': all_comments,
            'video': video
        })


