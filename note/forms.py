from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate


#form for auth user without using any shorcuts

class user_auth (forms.Form):
	user_name = forms.CharField(label='nickname', max_length=50)
	user_password = forms.CharField(label='password', max_length=100)



class user_registration (forms.Form):
	"""
	Form for user registration 
	fields:
		username
		password
		password_confirm
		email
	"""
	username = forms.CharField(label='nickname', max_length=50)
	password = forms.CharField(label='password', max_length=100)
	password_confirm = forms.CharField(label='password_confirm', max_length=100)
	email = forms.EmailField(label='email', max_length=50)
	

	# self.min_length = 6 #min_lenght for user/password
		

	def clean_username (self):
		"""
		Check for min length nickname
		"""
		if len(self.cleaned_data.get('username')) < 6:
			raise forms.ValidationError("Nickname to short", code = 'short_nick')

		return self.cleaned_data


	def clean_password(self):
		
		self.cleaned_data.get('password')

		if len(self.cleaned_data.get('password')) < 6:
			raise forms.ValidationError("Password to short", code = 'short_pass')

		# if lower(self.cleaned_data.get('password')) == self.cleaned_data.get('password') or upper(self.cleaned_data.get('password')) == self.cleaned_data.get('password'):
		# 	raise forms.ValidationError("Use diffrent literals for pas", code = 'liter_pas')

		return self.cleaned_data



	def clean_email (self):
		"""
		check email for unique
		"""
		try:
			User.objects.get(email = self.cleaned_data.get('email'))
			raise forms.ValidationError("Email already used", code = 'used_email')
		except User.DoesNotExist:
			return self.cleaned_data


	def clean(self):

		super().clean

		if self.cleaned_data.get('username') == self.cleaned_data.get('password'):
			raise forms.ValidationError("Password equal nickname", code = 'pass=nick')
		
		if self.cleaned_data.get('password') == self.cleaned_data.get('password_confirm'):
			raise forms.ValidationError("Password don't match", code = 'diff_pass')
		
		

		return self.cleaned_data


	def save(self):
		
		user_dict = self.cleaned_data.copy() #create a copy of dictionary clean_data
		del user_dict['password_confirm'] #remove a password confirm
		
		new_user = User.objects.create_user(**user_dict) #Create a user
		new_user.save()

		auth_dict = user_dict.copy()
		del auth_dict['email']

		auth_user = authenticate(**auth_dict)

		

		return auth_user