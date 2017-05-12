from django.conf.urls import include, url
from django.contrib import admin
from questions import views
from questions.models import Question
urlpatterns = [
    url(r'^admin/', include(admin.site.urls),name='admin'),
    url(r'^logout/', views.sign_out, name='logout'),
    url(r'^post/(?P<id>\d+)/$',Question.objects.getQuestionWithComments,name='post'),
    url(r'^posts/tag/(?P<tag>.*)/$',Question.objects.getQuestionsByTag,name='tag'),
    url(r'^signup/$', views.registration, name='signup'),
    url(r'^q/new/$', views.questions_list, name='new_q'),
    url(r'^q/trends/$', views.questions_list, name='hot_q'),
    url(r'^sign_in/$', views.sign_in, name='sign_in'),
    url(r'^comment_POST/$', views.post_comment, name='comment_POST'),
    url(r'^save_settings/$', views.save_settings, name='save_settings'),
    url(r'^question/post/$', views.post_question, name='postq'),
    url(r'^login/$', views.login,name='login'),
    url(r'^settings/$', views.settings,name='settings'),
    url(r'^logged/$', views.logged,name='logged'),
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^methods/',views.simpleapp, name='methods'),
    url(r'^$', views.questions_list, name='main')
]
