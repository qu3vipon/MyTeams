from django.contrib import admin

from .models import Team, Match, League


class TeamInline(admin.TabularInline):
    model = Team
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    inlines = [
        TeamInline,
    ]


admin.site.register(Match)
