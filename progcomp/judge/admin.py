from django.contrib import admin

from progcomp.judge.models import Grading
from progcomp.judge.models import Result


class GradingAdmin(admin.ModelAdmin):

    list_display = ('submission', 'grader', 'nonce', 'requested')


class ResultAdmin(admin.ModelAdmin):

    list_display = ('created', 'submission', 'status')


admin.site.register(Grading, GradingAdmin)
admin.site.register(Result, ResultAdmin)
