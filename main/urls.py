from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.urls import re_path

from . import views


app_name = 'main'
urlpatterns = [
	# re_path(r'^$', RedirectView.as_view(url='/main/', permanent=True)),
	re_path(r'^$', views.index, name='index'),
	re_path(r'^get_data_for_messages/', views.get_data_for_messages, name='get_data_for_messages'),
	re_path(r'^get_press/', views.get_press, name='get_press'),
	re_path(r'^get_message_for_waiting/', views.get_message_for_waiting, name='get_message_for_waiting'),
	re_path(r'^get_changed_language_content/', views.get_changed_language_content, name='get_changed_language_content'),
]