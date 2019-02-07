from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.urls import reverse


from .models import *
from .forms import *
from .views_func import *

def index(request):
	"""
	Main page
	"""
	notes=note_model.objects.all()
	
	context = {'notes':notes,
				'user': request.user}
	return render(request, 'note/index.html', context)

#Note page view, with menu
def note_view(request,slug):
	try:
		note = note_model.objects.get(slug__iexact=slug)
		
	except note_model.DoesNotExist:
		return redirect('main')
	
	notes = note_model.objects.all()
	context = {
		'notes':notes,
		'note': note,
		'user': request.user
		}
	return render(request, 'note/note_page.html', context)
	

class log_out(View):
	"""
	Log out link
	"""
	def get(self, request):
		return render(request, 'note/logout.html',{})

	def post(self, request):
		logout(request)
		return redirect('main')

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

	list_page(global_ident)

	
