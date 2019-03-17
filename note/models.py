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
		return reverse('note_detail', kwargs = {'slug' : self.slug})


	def __str__(self):
		return self.title



class Tag(models.Model):
	"""
	Tag for notes for searching
	"""
	tag = models.CharField(max_length = 50)

	def get_absolute_url(self):
		return reverse('tag_display', kwargs = {'tag': tag})


class Section(models.Model):
	
	"""
	Sections for notes
		1. Title - name of Section
		2. Description - short description for section
		3. global_id - unique identifer like User.Section.Section_id
		4. child index - index for define the location on the page
		5. num_child - quantity of direct childs for this section

		Relationships:
		6. creator - Many to One relationship with User
		7. parrent - Many to One relationship with parrent Section
	"""

	title = models.CharField(max_length = 50)
	description = models.CharField (max_length = 200, blank = True)
	global_id = models.CharField(max_length = 200, unique = True)	
	child_index = models.IntegerField(blank = True)
	

	#Relationship
	creator = models.ForeignKey(User, 
								on_delete = models.CASCADE)

	parrent = models.ForeignKey('self',
								on_delete = models.CASCADE,
								blank = True)

	def get_absolute_url(self):
		id_list = global_id.split('_')
		return reverse('section_view', kwargs = {'ident': id_list[2]})

	def get_absolute_url_create(self):
		id_list = global_id.split('_')
		return reverse('creating_object', kwargs = {'ident': id_list[2]})


class Notes(models.Model):
	"""
	Model for notes with next columns:
		1. title - Title of a note
		2. body_text - Main Text of the note
		3. pub_date - Publication Date
		5. global_id - global identifer like User.note.note_id
		6. child_index - int for define a location on the page
		
		Relationships		
		7. creator - Many to One relationship with Users
		8. parrent - Many to one relationship for parrent catalog
		9. tag - Many to Many relationship with tags
	"""
	title = models.CharField(max_length =  50)
	body_text = models.CharField(max_length = 500, blank = True)
	pub_date = models.DateField(auto_now = True)
	global_id = models.CharField(max_length = 200, unique = True)
	child_index = models.IntegerField()

	#Relationships
	creator = models.ForeignKey(User, 
								on_delete = models.CASCADE)

	parrent = models.ForeignKey(Section,
								on_delete = models.CASCADE,
								blank = True)

	tag = models.ManyToManyField(Tag)

	def get_absolute_url(self):
		id_list = global_id.split('_')
		return reverse('object_view', kwargs = {'ident': id_list[2]})




