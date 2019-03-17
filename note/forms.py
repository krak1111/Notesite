from django import forms
from django.contrib.auth.models import User 
from datetime import date
# from models import Section
from django.contrib.auth import authenticate, login
from utility.forms_func import child_count
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

		user_home_section = Section.create(title = 'Home', description = 'Home page',
									global_id = "%s_%s_%s" %(self.cleaned_data['username'], 'section', 'Home'),
									creator = self.cleaned_data['username'])

		user_home_section.save()

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
		full_tag_str = self.cleaned_data['tags']
		reg_template = re.compile(r"\b(\w+?)\b")

		clean_tag_list = reg.template.findall(full_tag_str)

		return clean_tag_list

	def clean_title(self):
		"""Title shouldn't have a #"""

		if '#' or '_' in self.cleaned_data['title']:
			raise forms.ValidationError("Title shouldn't have a # and _", code = 'not#_')
		else:
			return self.cleaned_data['title']


	def save(self, username, parrent_global_id):
		
		#Class for parrent section
		parrent_object = Section.objects.get(global_id = parrent_global_id)
		creator = User.objects.get(username = username)



		#Global id lookup username_note_title#index (index for title if this title already exist otherwise ='0')
		k = 0
		while True:
			global_ident = '%s_%s_%s', (username, 'note', ('title#%s',(k)))
			try:				
				Note.objects.get(global_id = global_ident)
				k+=1
			except Notes.DoesNoteExist:
				break

		create_date = date.today()

		creating_dict = {
			'title': self.cleaned_data['title'],
			'body_text': self.cleaned_data['body_text'],
			'pub_date': create_date,
			'global_id': global_ident,
			'child_index': child_count(parrent_global_id),
			'creator': creator,
			'parrent':parrent_object
		}
		note_object = Note.objects.create(kwargs = creating_dict)

		#Tag binding
		for current_tag in self.cleaned_data['tags']:
			try:
				note_object.tag.add(Tag.objects.get(tag__iexact = current_tag))
			except Tag.DoesNotExist:
				new_tag = Tag.objects.create(tag = current_tag).save()
				note_object.tag.add(new_tag)

		note_object.save()

		return note_object


class section_form(forms.Form):
	"""
		Form for create a section
		fields:
			1. title
			2. description
	"""
	title = forms.CharField(label = 'title', max_length = 50)
	description = forms.CharField(label = 'description', max_length = 150)

	def clean_title(self):
		"""Title shouldn't have a # or _"""

		if '#' or '_' in self.cleaned_data['title']:
			raise forms.ValidationError("Title shouldn't have a # and _", code = 'not#_')
		else:
			return self.cleaned_data['title']


	def save(self, username, parrent_global_id):
		
		#Class for parrent section
		parrent_object = Section.objects.get(global_id = parrent_global_id)
		creator = User.objects.get(username = username)

		#Global id lookup username_note_title#index (index for title if this title already exist otherwise ='0')
		k = 0
		while True:
			global_ident = '%s_%s_%s', (username, 'section', ('title#%s',(k)))
			try:				
				Section.objects.get(global_id = global_ident)
				k+=1
			except Section.DoesNoteExist:
				break

		

		creating_dict = {
			'title': self.cleaned_data['title'],
			'description': self.cleaned_data['description'],
			'global_id': global_ident,
			'child_index': child_count(parrent_global_id),			
			'creator': creator,
			'parrent':parrent_object
		}
		section_object = Section.objects.create(kwargs = creating_dict)

		section_object.save()

		return section_object






