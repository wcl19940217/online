from django.conf.urls import url
from .views import OrgView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView
from .views import TeacherListView, TeacherDetailView
from .views import AddUserAskView, AddFavView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="desc_course"),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="teacher_course"),
    # 机构搜藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
    # 课程讲师相关
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),
    # 课程讲师详情
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]
