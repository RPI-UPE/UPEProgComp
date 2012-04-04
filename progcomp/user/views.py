from django.http import HttpResponse
from django.shortcuts import render_to_response

from progcomp.judge.models import Result
from progcomp.account.models import is_registered

@is_registered
def diff(request, diffid):
	diff = Result.objects.all() \
				.filter(submission__registrant=request.user)#, id=diffid)
	return render_to_response(diff.diff.url)

def input(request, slug):
	response = HttpResponse(mimetype='application/force-download')
	return response
