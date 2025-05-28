# football_app/models.py

from django.db import models


# Tambahan untuk model yang sudah ada
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    village = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    name = models.CharField(max_length=100)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)  # For goalkeepers/defenders

    class Meta:
        unique_together = (
            "team",
            "name",
        )  # A player's name must be unique within a team

    @property
    def total_goals_assists(self):
        return self.goals + self.assists

    def __str__(self):
        return f"{self.name} ({self.team.name})"


class Match(models.Model):
    GROUP_CHOICES = [
        ("A", "Group A"),
        ("B", "Group B"),
        ("C", "Group C"),
        ("D", "Group D"),
        ("E", "Group E"),  # Jika ada lebih banyak grup
        ("F", "Group F"),
    ]

    STATUS_CHOICES = [
        ("Upcoming", "Akan Datang"),
        ("Finished", "Selesai"),
        ("Postponed", "Ditunda"),
        ("Cancelled", "Dibatalkan"),
    ]

    team1 = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="home_matches"
    )
    team2 = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="away_matches"
    )
    date = models.DateField()
    time = models.CharField(max_length=10)  # Contoh: "14:00 WIT"
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)
    matchday = models.IntegerField()
    score1 = models.IntegerField(null=True, blank=True)
    score2 = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Upcoming")

    class Meta:
        verbose_name_plural = "Matches"
        ordering = ["date", "time"]  # Default ordering
        unique_together = (
            "team1",
            "team2",
            "date",
            "time",
        )  # Prevent exact duplicate matches

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name} - Matchday {self.matchday}"
