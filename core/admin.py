# football_app/admin.py
from django.contrib import admin

from unfold.admin import TabularInline, ModelAdmin as UnfoldAdmin

from .models import Team, Player, Match


# Inline for Players within Team admin page
class PlayerInline(TabularInline):  # TabularInline is more compact for many players
    model = Player
    extra = 1  # Number of empty forms to display for new players
    fields = [
        "name",
        "goals",
        "assists",
        "clean_sheets",
    ]  # Fields to show in the inline form


@admin.register(Team)
class TeamAdmin(UnfoldAdmin):
    list_display = ("name", "village")
    search_fields = ("name", "village")
    inlines = [
        PlayerInline
    ]  # This line makes Player objects editable directly from the Team page


@admin.register(Player)
class PlayerAdmin(UnfoldAdmin):
    list_display = (
        "name",
        "team",
        "goals",
        "assists",
        "clean_sheets",
        "total_goals_assists",
    )
    list_filter = ("team",)  # Add filters on the right sidebar
    search_fields = (
        "name",
        "team__name",
    )  # Allow searching by player name or team name
    # readonly_fields = ('total_goals_assists',) # Display this calculated property as read-only


@admin.register(Match)
class MatchAdmin(UnfoldAdmin):
    list_display = (
        "__str__",
        "date",
        "time",
        "group",
        "status",
        "score1",
        "score2",
        "matchday",
    )
    list_filter = ("status", "group", "matchday", "date")  # Filters for matches
    search_fields = (
        "team1__name",
        "team2__name",
        "group",
    )  # Search by team names or group
    # Organize fields in the add/change form
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("team1", "team2"),
                    ("date", "time"),
                    "group",
                    "matchday",
                    "status",
                )
            },
        ),
        (
            "Hasil Pertandingan (Isi jika Selesai)",
            {
                "fields": (("score1", "score2"),),
                "classes": ("collapse",),  # This section will be collapsed by default
            },
        ),
    )
