# football_app/models.py

from django.db import models


# --- Model yang sudah ada (pastikan ini ada dan tidak berubah) ---
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    village = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Tim"
        verbose_name_plural = "Tim"

    def __str__(self):
        return self.name


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    name = models.CharField(max_length=100)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Pemain"
        verbose_name_plural = "Pemain"
        unique_together = ("team", "name")

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
        ("E", "Group E"),
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
    time = models.CharField(max_length=10)
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)
    matchday = models.IntegerField()
    score1 = models.IntegerField(null=True, blank=True)
    score2 = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Upcoming")

    class Meta:
        verbose_name = "Pertandingan"
        verbose_name_plural = "Pertandingan"
        ordering = ["date", "time"]
        unique_together = ("team1", "team2", "date", "time")

    def __str__(self):
        return f"Matchday {self.matchday} - {self.team1.name} vs {self.team2.name} ({self.date.strftime('%d %b')})"


# --- Model DataContribution (Diperbarui) ---
class DataContribution(models.Model):
    CONTRIBUTION_TYPE_CHOICES = [
        ("match_result", "Hasil Pertandingan"),
        ("player_stats", "Statistik Pemain (Gol/Assist)"),
        # Opsi 'new_team' dan 'other' dihapus
    ]

    contribution_type = models.CharField(
        max_length=20,
        choices=CONTRIBUTION_TYPE_CHOICES,
        help_text="Jenis data yang ingin Anda kontribusikan.",
    )

    contributor_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Tulis nama Anda (opsional).",
    )

    # --- Field Spesifik (tidak ada perubahan pada ini) ---
    match_to_update = models.ForeignKey(
        Match,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contributed_updates",
        help_text="Pilih pertandingan yang ingin Anda laporkan hasilnya.",
    )
    new_score1 = models.IntegerField(
        null=True, blank=True, help_text="Skor tim kandang yang baru."
    )
    new_score2 = models.IntegerField(
        null=True, blank=True, help_text="Skor tim tandang yang baru."
    )

    player_to_update = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contributed_updates",
        help_text="Pilih pemain yang statistiknya ingin Anda perbarui.",
    )
    goals_added = models.IntegerField(
        null=True,
        blank=True,
        default=0,
        help_text="Jumlah gol yang ingin ditambahkan (misal: 1, 2).",
    )
    assists_added = models.IntegerField(
        null=True,
        blank=True,
        default=0,
        help_text="Jumlah assist yang ingin ditambahkan (misal: 1, 2).",
    )

    # Field untuk 'new_team' dihapus:
    # proposed_team_name = models.CharField(max_length=100, blank=True, null=True, help_text="Nama tim baru yang ingin Anda usulkan.")
    # proposed_team_village = models.CharField(max_length=100, blank=True, null=True, help_text="Desa/Wilayah asal tim baru.")

    # Description tetap ada, karena bisa digunakan untuk detail tambahan pada kedua jenis kontribusi
    description = models.TextField(
        blank=True, help_text="Jelaskan detail kontribusi Anda. (opsional)"
    )

    STATUS_CHOICES = [
        ("pending", "Menunggu Kurasi"),
        ("approved", "Disetujui"),
        ("rejected", "Ditolak"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Data Kontribusi"
        verbose_name_plural = "Data Kontribusi"

    def __str__(self):
        return f"Kontribusi {self.get_contribution_type_display()} dari {self.contributor_name or 'Anonim'} - Status: {self.get_status_display()}"
