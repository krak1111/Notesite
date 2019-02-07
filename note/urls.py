from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name = 'main'),
	path('login/', views.user_login.as_view(), name='user_login'),
	path('logout/', views.log_out.as_view(), name = 'logout'),
	path('registration/', views.user_register.as_view(), name='user_registration'),
	path('not_exist/', views.not_exist, name = 'does_not_exist'),
	path('section/<str:ident>/', views.object_view, name = 'section_view'),
	path('section/<str:ident>/choose/', views.create_choose, name = 'create_choose_view'),
	path('section/<str:ident>/createsection/', views.create_section, name = 'create_section'),
	path('section/<str:ident>/createnote/', views.create_note, name = 'create_note'),
	path('note/<str:ident>', views.note_view, name = 'note_view'),
	path('note/<str:ident>/edit', views.note_edit, name = 'note_edit'),	
]