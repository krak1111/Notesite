from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.urls import reverse


from .models import *
from .forms import *
from utility.views_func import *

def index(request):
	"""
	Main page
	"""
	notes=note_model.objects.all()
	
	context = {'notes':notes,
				'user': request.user}
	return render(request, 'note/index.html', context)

#Log In view
class user_login(View):
	
	def get(self, request):
		if request.user.is_authenticated:
			return redirect('main')
		auth_form = user_auth()
		context = {'form': auth_form}
		return render(request, 'note/login.html', context)


	
	def post(self, request):
		
		if request.user.is_authenticated:
			return redirect('main')

		auth_dict = clear_from_csrf(request.POST)
		
		auth_form = user_auth(auth_dict)
		auth_form.is_valid()
		user = authenticate(request, **auth_form.cleaned_data)
		if user is not None:
			login(request, user)
			return redirect('main')
		else:
			context = {
						'form' :auth_form,
						'error': True
			}
			return render(request,'note/login.html',context)

#Log out
class log_out(View):
	"""
	Log out link
	"""
	def get(self, request):
		return render(request, 'note/logout.html',{})

	def post(self, request):
		logout(request)
		return redirect('main')
		
#Registration
class user_register(View):
	
	def get(self, request): #If get request wo only display form for registration
		
		reg_form = user_registration()
		context = {'form': reg_form}
		return render(request, 'note/register.html', context)


	
	def post(self, request):#Process a form
		
		req_dict = clear_from_csrf(request.POST)

		reg_form = user_registration(req_dict)
		tr = reg_form.is_valid()
		errors_values = reg_form.errors
		# data = request.POST
		if tr:
			
			user = reg_form.save(request)
			if user is not None:
				return redirect('main')

		context = {'form' : reg_form}			
		return render(request, 'note/register.html', context)


def section_view(request, ident):

	check_user(request)

	global_ident = '%s_%s_%s' %(request.user.username, 'section', ident)

	query_list = list_page(global_ident)
	
	context = {'content_objects': query_list,}

	if query_list:
		return render(request, 'note/section.html', context)
	else:
		return redirect('does_not_exist', kwargs = {'obj_type': 'section'})


def tag_display(request, s_tag):
	""" Tag searching"""
	check_user(request)

	try:
		context = {'content_objects': Notes.objects.filter(tag__iexact = s_tag)}
		return render(request, 'note/tag.html', context)
	except Notes.DoesNotExist:
		return redirect('does_not_exist', kwargs = {'obj_type': 'tag'})


def not_exist(request, obj_type):
	"""Page display a wrong searching"""
	check_user(request)

	context = {'obj_type': obj_type}

	return render(request, 'note/does_not_exist.html', context)


class create_view(View):
	"""
		View for object creating.
		Page include a choice (section or note)
	"""
	def get(self, request, ident):

		check_user(request)

		try:
			parrent_section = Section.objects.get(global_id = '%s_%s_%s', (request.user.username, 'section',ident))
		except Section.DoesNotExist:
			return redirect('does_not_exist', kwargs = {'obj_type': 'section'})

		context = {
			'note_form': note_form(),
			'section_form': section_form(),
			'parrent_section': parrent_section,
		}

		return render(request, 'note/create_object.html', context)

	def post(self, request, ident):

		check_user(request)
		global_ident = '%s_%s_%s', (request.user.username, 'section',ident)

		#
		try:
			parrent_section = Section.objects.get(global_id = global_ident)
		except Section.DoesNotExist:
			return redirect('does_not_exist', kwargs = {'obj_type': 'section'})
		
		clear_from_csrf(request.POST)

		#Initilization which form was send
		try:


		



#Note page view, with menu
def note_view(request, ident):
	""" View for single note """
	check_user(request)

	global_ident = '%s_%s_%s', (request.user.username,'note', ident)
	
	try:
		note_query = Notes.objects.get(global_id = global_ident)
		context = {'content_objects': note_query}
		return render(request, 'note/note_page.html', context)
	except:
		return redirect('does_not_exist', kwargs = {'obj_type':'note'})