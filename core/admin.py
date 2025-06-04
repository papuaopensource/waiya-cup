# football_app/admin.py
from django.contrib import admin

from unfold.admin import ModelAdmin as UnfoldAdmin

from .models import Team, Player, Match, DataContribution


# --- Admin Tim ---
@admin.register(Team)
class TeamAdmin(UnfoldAdmin):
    list_display = (
        "name",
        "village",
        "logo",
    )
    search_fields = (
        "name",
        "village",
    )
    # Tambahkan verbose_name untuk kolom
    list_display_links = ("name",)  # Makes the name clickable to edit


# --- Admin Pemain ---
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
    raw_id_fields = ("team",)  # Use raw_id_fields for ForeignKey if many teams


# --- Admin Pertandingan ---
@admin.register(Match)
class MatchAdmin(UnfoldAdmin):
    list_display = (
        "matchday",
        "group",
        "team1",
        "team2",
        "date",
        "time",
        "score1",
        "score2",
        "status",
    )
    list_filter = (
        "status",
        "group",
        "date",
        "matchday",
    )
    search_fields = (
        "team1__name",
        "team2__name",
        "group",
    )
    list_editable = (
        "score1",
        "score2",
        "status",
    )  # Allow direct editing of status and scores
    autocomplete_fields = ("team1", "team2")  # Use autocomplete for better UX
    date_hierarchy = "date"  # Add date hierarchy for easier navigation


# --- Admin Kontribusi Data ---
@admin.register(DataContribution)
class DataContributionAdmin(UnfoldAdmin):
    list_display = (
        "contribution_type",
        "contributor_name",
        "match_to_update",
        "new_score1",
        "new_score2",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "created_at",
    )
    search_fields = (
        "description",
        "contributor_name",
        "match_to_update__team1__name",
        "match_to_update__team2__name",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "contribution_type",
        "match_to_update",
        "new_score1",
        "new_score2",
        "description",
        "contributor_name",
    )
    fieldsets = (
        (
            "Informasi Kontribusi",
            {
                "fields": (
                    "contribution_type",
                    "contributor_name",
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
            },
        ),
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
