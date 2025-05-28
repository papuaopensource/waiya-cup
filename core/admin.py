# football_app/admin.py
from django.contrib import admin

from unfold.admin import TabularInline, ModelAdmin as UnfoldAdmin

from .models import (
    Team,
    Player,
    Match,
    DataContribution,
)  # Import DataContribution model


# Inline for Players within Team admin page
class PlayerInline(TabularInline):
    model = Player
    extra = 1
    fields = [
        "name",
        "goals",
        "assists",
        "clean_sheets",
    ]


@admin.register(Team)
class TeamAdmin(UnfoldAdmin):
    list_display = ("name", "village")
    search_fields = ("name", "village")
    inlines = [PlayerInline]


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
    list_filter = ("team",)
    search_fields = (
        "name",
        "team__name",
    )


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
    list_filter = ("status", "group", "matchday", "date")
    search_fields = (
        "team1__name",
        "team2__name",
        "group",
    )
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
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(DataContribution)
class DataContributionAdmin(UnfoldAdmin):
    list_display = (
        "contribution_type",
        "contributor_name",
        "contributor_email",
        "status",
        "created_at",
        "match_to_update",
        "player_to_update",
        # "proposed_team_name", # Dihapus
    )
    list_filter = (
        "contribution_type",
        "status",
        "created_at",
    )
    search_fields = (
        "description",
        "contributor_name",
        "contributor_email",
        "match_to_update__team1__name",
        "match_to_update__team2__name",
        "player_to_update__name",
        # "proposed_team_name", # Dihapus
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "contribution_type",
        "match_to_update",
        "new_score1",
        "new_score2",
        "player_to_update",
        "goals_added",
        "assists_added",
        # "proposed_team_name", # Dihapus
        # "proposed_team_village", # Dihapus
        "description",
        "contributor_name",
        "contributor_email",
    )
    fieldsets = (
        (
            "Informasi Kontribusi",
            {
                "fields": (
                    "contribution_type",
                    ("contributor_name", "contributor_email"),
                    "description",
                )
            },
        ),
        (
            "Detail Kontribusi Pertandingan",
            {
                "fields": (
                    "match_to_update",
                    ("new_score1", "new_score2"),
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Detail Kontribusi Statistik Pemain",
            {
                "fields": (
                    "player_to_update",
                    ("goals_added", "assists_added"),
                ),
                "classes": ("collapse",),
            },
        ),
        # "Detail Kontribusi Tim Baru" dihapus
        (
            "Status & Waktu",
            {
                "fields": (
                    "status",
                    ("created_at", "updated_at"),
                )
            },
        ),
    )
