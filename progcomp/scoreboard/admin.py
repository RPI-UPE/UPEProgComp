from django.contrib import admin

from progcomp.scoreboard.models import Scoreboard


class ScoreboardAdmin(admin.ModelAdmin): pass


admin.site.register(Scoreboard, ScoreboardAdmin)
