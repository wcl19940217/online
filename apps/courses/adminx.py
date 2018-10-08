from .models import Course, Lesson, Video, CoursesResource, BannerCourse
import xadmin
from organization.models import CourseOrg


# 批量添加,天下子目录下的文件，便捷嵌套
class LessonInline(object):
    model = Lesson
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums',
                    'get_zj_nums']
    search_fields = ['name', 'degree', 'learn_time']
    list_filter = ['name', 'degree', 'learn_time']
    ordering = ['-click_nums']  # 排列默认的规则
    readonly_fields = ['click_nums']   # 不可以编辑的
    list_editable = ['degree', 'desc']  # 选中的字段可以直接进行编辑,列表页可以直接修改
    exclude = ['fav_nums']  # 包括什么
    inlines = [LessonInline]   # 可以放多个
    refresh_times = [3, 5]  # 多长时间自动刷新一次
    style_fields = {"detail": "ueditor"}

    # 分类
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        """
        在保存课程的时候统计课程机构的课程数
        :return:
        """
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org)
            course_org.save()

        def post(self, request, *args, **kwargs):
            if 'excel' in request.FILES:
                pass
            return super(CourseAdmin, self).post(request, *args, **kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums']
    search_fields = ['name', 'degree', 'learn_time']
    list_filter = ['name', 'degree', 'learn_time']
    ordering = ['-click_nums']  # 排列默认的规则
    readonly_fields = ['click_nums']   # 不可以编辑的
    exclude = ['fav_nums']  # 包括什么
    inlines = [LessonInline]   # 可以放多个

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name']


class CoursesResourceAdmin(object):
    list_display = ['course', 'download', 'add_time']
    # search_fields = ['course', 'download']
    # list_filter = ['course',  'download']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CoursesResource, CoursesResourceAdmin)

