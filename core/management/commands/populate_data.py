# football_app/management/commands/populate_all_data.py
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from ...models import Team, Player, Match
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = "Populates the database with sample teams, players, and matches."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Memulai populasi data ---"))

        # --- 1. Populate Teams (Sama seperti sebelumnya) ---
        self.stdout.write(self.style.SUCCESS("\n--- Memulai populasi tim ---"))
        teams_to_create = [
            {"name": "FC Harapan", "village": "Kampung Bahagia"},
            {"name": "Perkasa United", "village": "Desa Maju"},
            {"name": "Bintang Timur FC", "village": "Dusun Cahaya"},
            {"name": "Gelora Indah", "village": "Kampung Damai"},
            {"name": "Cendrawasih FC", "village": "Pesisir Pantai"},
            {"name": "Elang Jaya", "village": "Bukit Tinggi"},
            {"name": "Merah Putih FC", "village": "Pusat Kota"},
            {"name": "Satria Muda", "village": "Perkampungan Lama"},
            {"name": "Garuda Sakti", "village": "Lembah Hijau"},
            {"name": "Singa Utara", "village": "Perkebunan Kopi"},
            {"name": "Rajawali FC", "village": "Tanjung Laut"},
            {"name": "Serigala Malam", "village": "Hutan Rimba"},
            {"name": "Banteng Merah", "village": "Dataran Rendah"},
            {"name": "Padi Emas FC", "village": "Sawah Luas"},
            {"name": "Pesona Alam", "village": "Danau Biru"},
            {"name": "Api Unggun FC", "village": "Gunung Berapi"},
            {"name": "Samudera Raya", "village": "Kepulauan Indah"},
            {"name": "Angkasa Biru", "village": "Langit Senja"},
        ]

        all_teams = []  # Untuk menyimpan objek tim yang berhasil dibuat
        for team_data in teams_to_create:
            try:
                team, created = Team.objects.get_or_create(
                    name=team_data["name"], defaults={"village": team_data["village"]}
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"  Berhasil membuat tim: {team.name}")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"  Tim sudah ada: {team.name}. Melewatkan.")
                    )
                all_teams.append(team)  # Tambahkan tim ke daftar
            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR(
                        f'  Gagal membuat tim {team_data["name"]} (nama sudah ada).'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'  Terjadi kesalahan saat membuat tim {team_data["name"]}: {e}'
                    )
                )
        self.stdout.write(self.style.SUCCESS("--- Populasi tim selesai ---"))

        # --- 2. Populate Players ---
        self.stdout.write(self.style.SUCCESS("\n--- Memulai populasi pemain ---"))
        if not all_teams:
            self.stdout.write(
                self.style.WARNING(
                    "Tidak ada tim yang ditemukan/dibuat. Melewatkan populasi pemain."
                )
            )
        else:
            player_names = [
                "Andi",
                "Budi",
                "Candra",
                "Dedi",
                "Eko",
                "Fajar",
                "Gilang",
                "Heri",
                "Irfan",
                "Joko",
                "Kiki",
                "Lian",
                "Maman",
                "Nana",
                "Oka",
                "Pandu",
                "Qori",
                "Rian",
                "Sasa",
                "Taufik",
                "Udin",
                "Vino",
                "Wati",
                "Xavier",
                "Yudi",
                "Zaky",
            ]
            for team in all_teams:
                # Membuat 15-20 pemain per tim
                num_players = random.randint(15, 20)
                for i in range(num_players):
                    player_name = (
                        random.choice(player_names) + f" {random.randint(1, 99)}"
                    )  # Tambah angka untuk unik
                    try:
                        # Randomkan nilai goals, assists, clean_sheets
                        goals = (
                            random.randint(0, 10) if random.random() > 0.3 else 0
                        )  # 70% chance to have goals
                        assists = (
                            random.randint(0, 5) if random.random() > 0.4 else 0
                        )  # 60% chance to have assists
                        clean_sheets = (
                            random.randint(0, 3) if random.random() > 0.7 else 0
                        )  # For goalkeepers, 30% chance

                        player, created = Player.objects.get_or_create(
                            team=team,
                            name=player_name,
                            defaults={
                                "goals": goals,
                                "assists": assists,
                                "clean_sheets": clean_sheets,
                            },
                        )
                        if created:
                            # self.stdout.write(self.style.SUCCESS(f'  Berhasil membuat pemain: {player.name} ({team.name})'))
                            pass  # Jangan terlalu banyak output untuk pemain
                    except IntegrityError:
                        # self.stdout.write(self.style.WARNING(f'  Pemain {player_name} sudah ada di {team.name}. Melewatkan.'))
                        pass  # Jangan terlalu banyak output untuk pemain
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"  Terjadi kesalahan saat membuat pemain {player_name} ({team.name}): {e}"
                            )
                        )
            self.stdout.write(self.style.SUCCESS("--- Populasi pemain selesai ---"))

        # --- 3. Populate Matches ---
        self.stdout.write(self.style.SUCCESS("\n--- Memulai populasi pertandingan ---"))
        if len(all_teams) < 2:
            self.stdout.write(
                self.style.WARNING(
                    "Tidak cukup tim untuk membuat pertandingan. Butuh minimal 2 tim."
                )
            )
        else:
            groups = [
                "A",
                "B",
                "C",
                "D",
            ]  # Sesuaikan dengan GROUP_CHOICES di model Anda
            time_slots = ["14:00 WIT", "16:00 WIT"]
            start_date = date.today() + timedelta(
                days=7
            )  # Mulai seminggu dari sekarang

            num_matches_per_matchday = (
                len(all_teams) // 2
            )  # Jika genap, setengah tim main tiap matchday

            for matchday in range(1, 6):  # Buat 5 matchday
                current_date = start_date + timedelta(
                    days=(matchday - 1) * 2
                )  # Setiap 2 hari ada matchday baru

                # Acak tim untuk setiap matchday agar bervariasi
                random.shuffle(all_teams)

                # Pastikan tim yang bermain berbeda
                teams_for_matchday = list(all_teams)

                # Buat pertandingan
                for i in range(num_matches_per_matchday):
                    if len(teams_for_matchday) < 2:
                        break  # Tidak cukup tim tersisa

                    team1 = teams_for_matchday.pop(0)
                    team2 = teams_for_matchday.pop(0)

                    # Randomkan status dan skor
                    status = "Upcoming"
                    score1 = None
                    score2 = None

                    if matchday <= 3:  # Misal, matchday 1-3 sudah selesai
                        status = "Finished"
                        score1 = random.randint(0, 5)
                        score2 = random.randint(0, 5)
                        # Pastikan tidak ada skor sama jika salah satu tim menang
                        while (
                            score1 == score2 and random.random() < 0.3
                        ):  # 30% chance of draw
                            score2 = random.randint(
                                0, 5
                            )  # re-roll if draw and we want a winner

                    group_assigned = random.choice(groups)  # Acak grup

                    try:
                        match, created = Match.objects.get_or_create(
                            team1=team1,
                            team2=team2,
                            date=current_date,
                            time=random.choice(time_slots),
                            matchday=matchday,
                            defaults={
                                "group": group_assigned,
                                "status": status,
                                "score1": score1,
                                "score2": score2,
                            },
                        )
                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"  Berhasil membuat pertandingan: {match.team1.name} vs {match.team2.name} (MD{matchday})"
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"  Pertandingan {match.team1.name} vs {match.team2.name} (MD{matchday}) sudah ada. Melewatkan."
                                )
                            )
                    except IntegrityError:
                        self.stdout.write(
                            self.style.ERROR(
                                f"  Gagal membuat pertandingan antara {team1.name} dan {team2.name} (MD{matchday}) karena duplikasi."
                            )
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"  Terjadi kesalahan saat membuat pertandingan ({team1.name} vs {team2.name}): {e}"
                            )
                        )

        self.stdout.write(self.style.SUCCESS("--- Populasi pertandingan selesai ---"))
        self.stdout.write(
            self.style.SUCCESS("\n--- Populasi data selesai sepenuhnya! ---")
        )
