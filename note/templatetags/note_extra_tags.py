from django import template
import re

register = template.Library()

@register.filter
def obj_type(value):

	try:
		value.pub_date
		return 'note'

	except AttributeError:
		return 'section'

	return None


