from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.questions_list, name='questions_list')
]