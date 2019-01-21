from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User 


class note_model(models.Model):
	title = models.CharField(max_length=50, db_index=True)
	slug = models.SlugField(max_length=50, unique=True)
	body = models.CharField(max_length=300)
	pub_data = models.DateTimeField(auto_now_add=True)
	#creator = models.CharField(max_length=50)

	def get_absolute_url(self):
		return reverse('note_detail', kwargs={'slug':self.slug})


	def __str__(self):
		return self.title

# class Custom_User(User): #Create unique email
# 	email = models.EmailField(max_length = 60, unique = True)