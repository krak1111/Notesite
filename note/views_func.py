"""
	Functions for views.py for anything
"""
def clear_from_csrf(dict):
	"""
	remove from request.POST csrf token
	"""
	cleared_dict = dict.copy()
	del cleared_dict['csrfmiddlewaretoken']

	return cleared_dict


def check_user(request):
	if not request.user.is_authenticated():
		return redirect('user_login')
	pass


def list_page(global_ident):
	"""
	Create a unordered list of objects to show on the page
	"""
	#Validate an object
	try:		
		Section.objects.get(global_id = dlobal_ident)

	except Section.DoesNotExist:
		redirect ('does_not_exist')

	#prepare a list of queries for display
	try:	
		Section_query = Section.objects.filter(parrent = parrent_globalid)

		try:
			notes_query = Notes.objects.filter(parrent = parrent_globalid)
			# union a quries
			union_query = section_query.union(notes_query)
			return union_query

		except Notes.DoesNotExist:
			return section_query

	except Section.DoesNotExist:
		return None
	

	

