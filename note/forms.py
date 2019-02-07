from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login
import re


#form for auth user without using any shorcuts

class user_auth (forms.Form):
	username = forms.CharField(label='username', max_length=50)
	password = forms.CharField(label='password', max_length=100)


class user_registration (forms.Form):
	"""
	Form for user registration 
	fields:
		username
		password
		password_confirm
		email
	"""
	username = forms.CharField(label='username', max_length=50)
	password = forms.CharField(label='password', max_length=100)
	password_confirm = forms.CharField(label='password_confirm', max_length=100)
	email = forms.EmailField(label='email', max_length=50)
	

	# self.min_length = 6 #min_lenght for user/password
		

	def clean_username (self):
		"""
		Check for min length nickname
		"""
		us = self.cleaned_data.get('username')
		if len(us) < 6:
			raise forms.ValidationError("Nickname to short", code = 'short_nick')

		try:
			User.objects.get(username = us)
			raise forms.ValidationError("Nicname is already used", code = 'used_user')
		except: User.DoesNotExist

		return us


	def clean_password(self):
		
		pas = self.cleaned_data.get('password')

		if len(pas) < 6:
			raise forms.ValidationError("Password to short", code = 'short_pass')

		if pas.lower() == pas or pas.upper()== pas:
			raise forms.ValidationError("Use diffrent literals for pas", code = 'liter_pas')

		return pas


	
	def clean_email (self):
		"""
		check email for unique
		"""
		cleaned_email = self.cleaned_data.get('email')
		try:
			User.objects.get(email = cleaned_email )
			raise forms.ValidationError("Email already used", code = 'used_email')
		except User.DoesNotExist:

			return cleaned_email


	def clean(self):

		super().clean

		if self.cleaned_data.get('username') == self.cleaned_data.get('password') and self.cleaned_data.get('username') is not None:
			raise forms.ValidationError("Password equal nickname", code = 'pass=nick')
		
		if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirm') and self.cleaned_data.get('password') is not None:
			raise forms.ValidationError("Password don't match", code = 'diff_pass')
		
		

		return self.cleaned_data


	def save(self,request):
		
		user_dict = self.cleaned_data.copy() #create a copy of dictionary clean_data
		del user_dict['password_confirm'] #remove a password confirm
		
		new_user = User.objects.create_user(**user_dict) #Create a user
		new_user.save()

		auth_dict = user_dict.copy()
		del auth_dict['email']

		auth_user = authenticate(**auth_dict)
		login(request, auth_user)

		

		return auth_user


class notes_form(forms.Form):
	"""
	Form for create notes
	Fields:
		1. Title
		2. Body text
		3. Tags
	"""
	title = forms.CharField(label = 'title', max_length = 50)
	body_text = forms.CharField(label = 'body_text', max_length = 500)
	tags = forms.CharField(label = 'tags', max_length = 200)

	def clean_tags(self):
		"""
			tags raw is a string like "history flame user" 
				or
			"history, flame, user"
				or
			"history. flame. user" 
		"""
		full_tag_str = self.clean_data['tags']
		reg_template = re.compile(r"\b(\w+?)\b")

		clean_tag_list = reg.template.findall(full_tag_str)

		return clean_tag_list

	def save(self, parrent_globalid = blank, ):
		pass

