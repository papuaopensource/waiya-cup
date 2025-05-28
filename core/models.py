# football_app/models.py

from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nama Tim")
    village = models.CharField(max_length=100, verbose_name="Asal Desa")

    class Meta:
        verbose_name = "Tim"
        verbose_name_plural = "Tim-tim"

    def __str__(self):
        return self.name


class Player(models.Model):
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="players", verbose_name="Tim"
    )
    name = models.CharField(max_length=100, verbose_name="Nama Pemain")
    goals = models.IntegerField(default=0, verbose_name="Gol")
    assists = models.IntegerField(default=0, verbose_name="Assist")
    clean_sheets = models.IntegerField(default=0, verbose_name="Clean Sheet")

    class Meta:
        unique_together = ("team", "name")
        verbose_name = "Pemain"
        verbose_name_plural = "Pemain-pemain"

    @property
    def total_goals_assists(self):
        return self.goals + self.assists

    def __str__(self):
        return f"{self.name} ({self.team.name})"


class Match(models.Model):
    GROUP_CHOICES = [
        ("A", "Grup A"),
        ("B", "Grup B"),
        ("C", "Grup C"),  # Ubah ke BI
        ("D", "Grup D"),
        ("E", "Grup E"),
        ("F", "Grup F"),
    ]

    STATUS_CHOICES = [
        ("Upcoming", "Akan Datang"),
        ("Finished", "Selesai"),
        ("Postponed", "Ditunda"),
        ("Cancelled", "Dibatalkan"),
    ]

    team1 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="home_matches",
        verbose_name="Tim Kandang",
    )
    team2 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="away_matches",
        verbose_name="Tim Tandang",
    )
    date = models.DateField(verbose_name="Tanggal")
    time = models.CharField(max_length=10, verbose_name="Waktu")
    group = models.CharField(max_length=1, choices=GROUP_CHOICES, verbose_name="Grup")
    matchday = models.IntegerField(verbose_name="Matchday")
    score1 = models.IntegerField(null=True, blank=True, verbose_name="Skor Tim Kandang")
    score2 = models.IntegerField(null=True, blank=True, verbose_name="Skor Tim Tandang")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Upcoming",
        verbose_name="Status Pertandingan",
    )

    class Meta:
        verbose_name = "Pertandingan"
        verbose_name_plural = "Pertandingan-pertandingan"
        ordering = ["date", "time"]
        unique_together = ("team1", "team2", "date", "time")

    def __str__(self):
        return f"Matchday {self.matchday} - {self.team1.name} vs {self.team2.name} ({self.date.strftime('%d %b')})"


class DataContribution(models.Model):
    CONTRIBUTION_TYPE_CHOICES = [
        ("match_result", "Hasil Pertandingan"),
    ]

    contribution_type = models.CharField(
        max_length=20,
        choices=CONTRIBUTION_TYPE_CHOICES,
        default="match_result",
        verbose_name="Jenis Kontribusi",
        help_text="Jenis data yang dikontribusikan (otomatis: Hasil Pertandingan).",
    )

    contributor_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Nama Kontributor",
        help_text="Nama Anda (opsional)",
    )

    match_to_update = models.ForeignKey(
        Match,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="contributed_match_updates",
        verbose_name="Pertandingan yang Diperbarui",
        help_text="Pilih pertandingan yang ingin Anda laporkan hasilnya.",
    )
    new_score1 = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Skor Baru Tim Kandang",
        help_text="Skor tim kandang yang baru.",
    )
    new_score2 = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Skor Baru Tim Tandang",
        help_text="Skor tim tandang yang baru.",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Deskripsi Tambahan",
        help_text="Jelaskan detail kontribusi Anda (misal: daftar pemain pencetak gol atau assist).",
    )

    STATUS_CHOICES = [
        ("pending", "Menunggu Kurasi"),
        ("approved", "Disetujui"),
        ("rejected", "Ditolak"),
    ]
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending", verbose_name="Status"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui Pada")

    class Meta:
        verbose_name = "Kontribusi Data"
        verbose_name_plural = "Kontribusi Data"

    def __str__(self):
        return f"Kontribusi Hasil Pertandingan dari {self.contributor_name or 'Anonim'} - {self.match_to_update or 'Tidak Ada Pertandingan'} - Status: {self.get_status_display()}"
