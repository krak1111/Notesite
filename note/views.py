from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.urls import reverse


from .models import *
from .forms import*

#Main Page View with all notes
def index(request):
	notes=note_model.objects.all()
	context = {'notes':notes,}
	return render(request, 'note/index.html', context)

#Note page view, with menu
def note_view(request,slug):
	note = note_model.objects.get(slug__iexact=slug)
	notes = note_model.objects.all()
	context = {
		'navigation':notes,
		'note': note,
	}
	return render(request, 'note/note_page.html', context)

#Log In view
class user_login(View):
	
	def get(self, request):
		auth_form = user_auth()
		context = {'form': auth_form}
		return render(request, 'note/login.html', context)

	def post(self, request):
		auth_form = user_auth(request.POST)
		user = authenticate(request, username = auth_form.clean_data['user_name'], 
								  password = auth_form.clean_data['user_password'])
		try:
			if user is not None:
				user.login(request, user)
				return redirect(reverse('main'))
		except:
			return render(request.POST)
		
#Registration
class user_register(View):

	def get(self, request): #If get request wo only display form for registration
		reg_form = user_registration()
		context = {'form': reg_form}
		return render(request, 'note/register.html', context)

	def post(self, request):#Process a form
		reg_form = user_registration(request.POST)
		tr = reg_form.is_valid()
		data = reg_form.cleaned_data
		if tr:
			
			user = reg_form.save()
			if user is not None:
				return redirect('index')

		context = {'form' : reg_form,
					'data': list(data.keys())}			
		return render(request, 'note/register.html', context)