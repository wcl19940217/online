from django.db import models
from datetime import datetime
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField
# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    # detail = models.TextField(verbose_name=u"课程详情")
    detail = UEditorField(verbose_name=u"课程详情", width=600, height=300, toolbars="full",
                                         imagePath="courses/ueditor/", filePath="courses/ueditor/", default='')
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)
    degree = models.CharField(choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(max_length=20, verbose_name=u"课程类别", default=u"后端开发")
    tag = models.CharField(default='', verbose_name=u"课程标签", max_length=10)
    youneed_know = models.CharField(max_length=300, verbose_name=u"课程须知", default='')
    teacher_tell = models.CharField(max_length=300, verbose_name=u"老师告诉你", default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lesson_set.all().count()
    get_zj_nums.short_description = "章节数"  # 显示章节数

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='www.baidu.com'>跳转</>")
    get_zj_nums.short_description = "跳转"  # 自定义跳转HTML

    def get_learn_users(self):
        return self.usercourse_set.all()

    def get_course_lesson(self):
        return self.lesson_set.all()

    def __repr__(self):
        return self.name

    __str__ = __repr__


class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True   # 不会生成表，只是admin注册


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名", default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.name

    __str__ = __repr__

    def get_lesson_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    url = models.CharField(max_length=200, verbose_name=u"访问地址", default='')
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.name

    __str__ = __repr__


class CoursesResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="下载地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"资源下载"
        verbose_name_plural = verbose_name

    def __repr__(self):
        return self.name

    __str__ = __repr__

