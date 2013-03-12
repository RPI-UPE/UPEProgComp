from django.contrib import admin

from progcomp.scoreboard.models import ScoreboardAccess



class ScoreboardAccessAdmin(admin.ModelAdmin):
    fieldsets = (None, {
        'fields': ('purpose',)
    }),
    list_display = ('code', 'purpose', 'visits')


admin.site.register(ScoreboardAccess, ScoreboardAccessAdmin)
