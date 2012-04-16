from django.contrib import admin

from progcomp.submission.models import Submission
from progcomp.submission.models import Attempt



class SubmissionAdmin(admin.ModelAdmin):

    list_display = ('registrant', 
            'submitted', 'sourcecode','output_file','attempt')

class AttemptAdmin(admin.ModelAdmin):
    
    list_display = ('person', 'problem', 'startTime', 'inputCases')


admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Attempt, AttemptAdmin)
