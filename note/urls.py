from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name = 'main'),#+
	path('login/', views.user_login.as_view(), name='user_login'),#+
	path('logout/', views.log_out.as_view(), name = 'logout'),#+
	path('registration/', views.user_register.as_view(), name='user_registration'),#+
	path('<str:slug>/', views.note_view, name = 'note_detail'),
	path('tag/<str:tag>/', views.tag_view, name = 'tag_display'),#+
	path('not_exist/<str:obj_type>/', views.not_exist, name = 'does_not_exist'),#+
	path('section/<str:ident>/', views.object_view, name = 'section_view'), #+
	path('section/<str:ident>/creating/', views.create_view.as_view(), name = 'create_view'),
	path('section/<str:ident>/edit/', views.section_edit.as_view(), name = 'section_edit'),
	path('note/<str:ident>/', views.note_view, name = 'note_view'), #+
	path('note/<str:ident>/edit/', views.note_edit, name = 'note_edit'),	
]