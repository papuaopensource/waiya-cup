# football_app/models.py
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nama Tim")
    village = models.CharField(max_length=100, verbose_name="Asal Kampung")

    class Meta:
        ordering = ["name"]  # Order teams alphabetically by default
        verbose_name = "Tim"
        verbose_name_plural = "Tim"

    def __str__(self):
        return self.name


class Player(models.Model):
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="players", verbose_name="Tim"
    )
    name = models.CharField(max_length=100, verbose_name="Nama Pemain")
    goals = models.PositiveIntegerField(default=0, verbose_name="Gol")
    assists = models.PositiveIntegerField(default=0, verbose_name="Assist")
    clean_sheets = models.PositiveIntegerField(
        default=0, verbose_name="Clean Sheet"
    )  # For goalkeepers

    class Meta:
        ordering = ["name"]  # Default ordering for players
        verbose_name = "Pemain"
        verbose_name_plural = "Pemain"
        unique_together = (
            "team",
            "name",
        )  # A player name should be unique within a team

    def __str__(self):
        return f"{self.name} ({self.team.name})"

    @property
    def total_goals_assists(self):
        """Calculates combined goals and assists for the player."""
        return self.goals + self.assists


class Match(models.Model):
    GROUP_CHOICES = [
        ("A", "Grup A"),
        ("B", "Grup B"),
        ("C", "Grup C"),
        ("D", "Grup D"),
        # Add more groups as needed
    ]
    STATUS_CHOICES = [
        ("Upcoming", "Akan Datang"),
        ("Finished", "Selesai"),
        ("Live", "Sedang Berlangsung"),
        ("Cancelled", "Dibatalkan"),
    ]

    team1 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="home_matches",
        verbose_name="Tim 1",
    )
    team2 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="away_matches",
        verbose_name="Tim 2",
    )
    date = models.DateField(verbose_name="Tanggal")
    time = models.CharField(max_length=10, verbose_name="Waktu")  # e.g., "14:00 WIT"
    score1 = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Skor Tim 1"
    )
    score2 = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Skor Tim 2"
    )
    group = models.CharField(max_length=1, choices=GROUP_CHOICES, verbose_name="Grup")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="Upcoming", verbose_name="Status"
    )
    matchday = models.PositiveIntegerField(default=1, verbose_name="Matchday ke-")

    class Meta:
        ordering = [
            "matchday",
            "date",
            "time",
        ]  # Order matches by matchday, then date, then time
        verbose_name = "Pertandingan"
        verbose_name_plural = "Pertandingan"
        # Prevent exact duplicate matches
        unique_together = ("team1", "team2", "date", "time")

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name} (Matchday {self.matchday})"

    # Helper methods (optional, but good for logic in views/templates)
    def get_winner(self):
        if (
            self.status == "Finished"
            and self.score1 is not None
            and self.score2 is not None
        ):
            if self.score1 > self.score2:
                return self.team1
            elif self.score2 > self.score1:
                return self.team2
        return None

    def get_loser(self):
        if (
            self.status == "Finished"
            and self.score1 is not None
            and self.score2 is not None
        ):
            if self.score1 < self.score2:
                return self.team1
            elif self.score2 < self.score1:
                return self.team2
        return None

    def is_draw(self):
        return (
            self.status == "Finished"
            and self.score1 is not None
            and self.score2 is not None
            and self.score1 == self.score2
        )
