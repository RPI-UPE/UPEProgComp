from django.contrib import admin

from progcomp.problems.models import Problem
from progcomp.problems.forms import ProblemForm


class ProblemAdmin(admin.ModelAdmin):

    list_display = ('slug', 'name','number_in_problem','number_test')
    form = ProblemForm


admin.site.register(Problem, ProblemAdmin)
