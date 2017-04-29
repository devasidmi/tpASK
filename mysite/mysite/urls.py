from django.conf.urls import include, url
from django.contrib import admin
from questions import views
from questions.models import Question
urlpatterns = [
    url(r'^admin/', include(admin.site.urls),name='admin'),
    url(r'^post/(?P<id>\d+)/$',Question.objects.getQuestionWithComments,name='post'),
    url(r'^posts/tag/(?P<tag>\D+)/$',Question.objects.getQuestionsByTag,name='tag'),
    url(r'^signup/$', views.registration, name='signup'),
    url(r'^login/$', views.login,name='login'),
    url(r'^settings/$', views.settings,name='settings'),
    url(r'^logged/$', views.logged,name='logged'),
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^methods/',views.simpleapp, name='methods'),
    url(r'^$', views.questions_list, name='main')
]
