from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name = 'main'),
	path('login/', views.user_login.as_view(), name='user_login'),
	path('registration/', views.user_register.as_view(), name='user_registration'),
	path('<str:slug>/', views.note_view, name='note_detail'),
]