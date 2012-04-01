from django.contrib import admin

from progcomp.judge.models import Result

class ResultAdmin(admin.ModelAdmin):

    list_display = ('created', 'submission', 'status', 'diff')


admin.site.register(Result, ResultAdmin)
