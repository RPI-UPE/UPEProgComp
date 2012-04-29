from django.template import Library

register = Library()

statuses = {
	'success': '',
	'failed': 'Most recent incorrect answer',
	'invalid': 'Correct answer submitted after competition end',
	'success first': 'First user to submit a correct solution to this problem',
}

@register.filter
def status_text(status):
	if status in statuses:
		return statuses[status]
	return status
