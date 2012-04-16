from django.contrib import admin

from progcomp.account.models import Profile
from progcomp.account.forms import AdminForm


class ProfileAdmin(admin.ModelAdmin):

    list_display = ('user','first_name','last_name', 'grad')
    form = AdminForm
    #exclude = ['user']


admin.site.register(Profile, ProfileAdmin)
