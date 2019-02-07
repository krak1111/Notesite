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

def list_page( is_note = False, parrent_globalid = None):
	"""
	Create a list of objects to show on the page
	"""
	# Validation url earlier into view
	try:
		#Query for the childrens of folder
		section_query = Section.objects.filter(parrent = parrent_globalid)
		try:
			notes_query = Notes.objects.filter(parrent = parrent_globalid)
			# union a quries
			union_query = section_query.union(notes_query).order_by('child_index')
			return union_query

		except Notes.DoesNotExist:
			return section_query

	except Section.DoesNotExist:
		try:
			note_query = Notes.objects.get(global_id = parrent_globalid)
			return note_query
		except Notes.DoesNotExist:
			return None

	if is_note:
		note_query = Notes.objects.get(global_id = parrent_globalid)
		return note_query

	else:
		try:
			section_query = Section.objects.filter(parrent = parrent_globalid)
			try:
				notes_query = Notes.objects.filter(parrent = parrent_globalid)
				# union a quries
				union_query = section_query.union(notes_query).order_by('child_index')
				return union_query

			except Notes.DoesNotExist:
				return section_query

		except  


