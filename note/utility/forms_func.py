#Utility func for forms
from .views_func import list_page

def child_count(parrent_global_id):
	"""Child id lookup"""

	child_list = list_page(parrent_global_id)		
	if child_list:
		object_count = child_list.count()+1
	else:
		object_count = 1

	return object_count