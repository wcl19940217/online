from .models import Course, Lesson, Video, CoursesResource
import xadmin


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'image', 'click_nums']
    search_fields = ['name', 'degree', 'learn_time']
    list_filter = ['name', 'degree', 'learn_time']


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
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CoursesResource, CoursesResourceAdmin)

