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

        # --- 1. Populate Teams with Group Assignments ---
        self.stdout.write(self.style.SUCCESS("\n--- Memulai populasi tim ---"))

        # Group A teams (index 0-11: Kalsor FC to Pase Putra)
        group_a_teams = [
            {"name": "Kalsor FC", "village": "Kampung Bahagia"},
            {"name": "Persebu FC", "village": "Desa Maju"},
            {"name": "Porambu FC", "village": "Dusun Cahaya"},
            {"name": "Swis FC", "village": "Kampung Damai"},
            {"name": "Portas FC", "village": "Pesisir Pantai"},
            {"name": "Waiya Jr", "village": "Bukit Tinggi"},
            {"name": "Bemta FC", "village": "Pusat Kota"},
            {"name": "PSK Kendate", "village": "Perkampungan Lama"},
            {"name": "Arema FC", "village": "Kampung Maribu"},
            {"name": "Dobukuring FC", "village": "Perkebunan Kopi"},
            {"name": "PAS Demoi", "village": "Tanjung Laut"},
            {"name": "Pase Putra", "village": "Hutan Rimba"},
        ]

        # Group B teams (index 12-23: Astor FC to Wasa FC)
        group_b_teams = [
            {"name": "Astor FC", "village": "Dataran Rendah"},
            {"name": "Setan Merah", "village": "Sawah Luas"},
            {"name": "Red wine Jr", "village": "Danau Biru"},
            {"name": "Waiya Putra", "village": "Gunung Berapi"},
            {"name": "Sokisi Putra", "village": "Kepulauan Indah"},
            {"name": "Star Seroyena", "village": "Langit Senja"},
            {"name": "Sebics FC", "village": "Padang Terang"},
            {"name": "Kerikil Putra", "village": "Batu Kerikil"},
            {"name": "Bambar Jr", "village": "Tepi Bukit"},
            {"name": "Tanah Merah FC", "village": "Tanah Merah"},
            {"name": "PS Pasti", "village": "Desa Pasti"},
            {"name": "Wasa FC", "village": "Lembah Wasa"},
        ]

        all_teams = []  # Untuk menyimpan objek tim yang berhasil dibuat
        team_groups = {}  # Untuk menyimpan mapping tim ke grup

        # Create Group A teams
        for team_data in group_a_teams:
            try:
                team, created = Team.objects.get_or_create(
                    name=team_data["name"], defaults={"village": team_data["village"]}
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  Berhasil membuat tim Grup A: {team.name}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"  Tim sudah ada: {team.name}. Melewatkan.")
                    )
                all_teams.append(team)
                team_groups[team] = "A"  # Assign to Group A
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

        # Create Group B teams
        for team_data in group_b_teams:
            try:
                team, created = Team.objects.get_or_create(
                    name=team_data["name"], defaults={"village": team_data["village"]}
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  Berhasil membuat tim Grup B: {team.name}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"  Tim sudah ada: {team.name}. Melewatkan.")
                    )
                all_teams.append(team)
                team_groups[team] = "B"  # Assign to Group B
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

        self.stdout.write(
            self.style.SUCCESS(
                f"--- Populasi tim selesai (Total: {len(all_teams)} tim) ---"
            )
        )

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
                "Ahmad",
                "Bayu",
                "Cahya",
                "Dimas",
                "Erick",
                "Fauzi",
                "Gandi",
                "Haris",
                "Ivan",
                "Johan",
                "Kevin",
                "Lucky",
                "Mario",
                "Nanda",
            ]

            for team in all_teams:
                # Membuat 15-20 pemain per tim
                num_players = random.randint(15, 20)
                used_names = set()  # Untuk memastikan nama unik dalam tim

                for i in range(num_players):
                    # Generate unique name untuk tim ini
                    attempts = 0
                    while attempts < 50:  # Maksimal 50 percobaan
                        base_name = random.choice(player_names)
                        player_name = f"{base_name} {random.randint(1, 99)}"
                        if player_name not in used_names:
                            used_names.add(player_name)
                            break
                        attempts += 1

                    if attempts >= 50:
                        player_name = f"Player {i+1} {team.name[:3]}"

                    try:
                        # Randomkan nilai goals, assists, clean_sheets
                        goals = random.randint(0, 10) if random.random() > 0.3 else 0
                        assists = random.randint(0, 5) if random.random() > 0.4 else 0
                        clean_sheets = (
                            random.randint(0, 3) if random.random() > 0.7 else 0
                        )

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
                            pass  # Jangan terlalu banyak output untuk pemain
                    except IntegrityError:
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
            time_slots = ["14:00", "16:00"]
            start_date = date.today() + timedelta(
                days=7
            )  # Mulai seminggu dari sekarang

            # Separate teams by group for matches
            group_a_teams_obj = [
                team for team in all_teams if team_groups.get(team) == "A"
            ]
            group_b_teams_obj = [
                team for team in all_teams if team_groups.get(team) == "B"
            ]

            # Create matches within each group
            for group_name, teams_in_group in [
                ("A", group_a_teams_obj),
                ("B", group_b_teams_obj),
            ]:
                if len(teams_in_group) < 2:
                    continue

                self.stdout.write(
                    self.style.SUCCESS(
                        f"\n  Membuat pertandingan untuk Grup {group_name}:"
                    )
                )

                for matchday in range(1, 6):  # Buat 5 matchday
                    current_date = start_date + timedelta(days=(matchday - 1) * 2)

                    # Shuffle teams untuk variasi pertandingan
                    teams_copy = list(teams_in_group)
                    random.shuffle(teams_copy)

                    # Buat pertandingan dalam grup
                    matches_created = 0
                    max_matches_per_day = len(teams_copy) // 2

                    for i in range(0, len(teams_copy) - 1, 2):
                        if matches_created >= max_matches_per_day:
                            break

                        if i + 1 < len(teams_copy):
                            team1 = teams_copy[i]
                            team2 = teams_copy[i + 1]

                            # Randomkan status dan skor
                            status = "Upcoming"
                            score1 = None
                            score2 = None

                            if matchday <= 3:  # Matchday 1-3 sudah selesai
                                status = "Finished"
                                score1 = random.randint(0, 5)
                                score2 = random.randint(0, 5)
                                # 30% chance untuk seri
                                if random.random() > 0.3 and score1 == score2:
                                    score2 = random.randint(0, 5)

                            try:
                                match, created = Match.objects.get_or_create(
                                    team1=team1,
                                    team2=team2,
                                    date=current_date,
                                    time=random.choice(time_slots),
                                    matchday=matchday,
                                    defaults={
                                        "group": group_name,
                                        "status": status,
                                        "score1": score1,
                                        "score2": score2,
                                    },
                                )
                                if created:
                                    self.stdout.write(
                                        self.style.SUCCESS(
                                            f"    Grup {group_name} MD{matchday}: {match.team1.name} vs {match.team2.name}"
                                        )
                                    )
                                    matches_created += 1
                                else:
                                    self.stdout.write(
                                        self.style.WARNING(
                                            f"    Pertandingan {match.team1.name} vs {match.team2.name} (MD{matchday}) sudah ada."
                                        )
                                    )
                            except IntegrityError:
                                self.stdout.write(
                                    self.style.ERROR(
                                        f"    Gagal membuat pertandingan {team1.name} vs {team2.name} (MD{matchday})"
                                    )
                                )
                            except Exception as e:
                                self.stdout.write(
                                    self.style.ERROR(
                                        f"    Error: {team1.name} vs {team2.name} - {e}"
                                    )
                                )

        self.stdout.write(self.style.SUCCESS("--- Populasi pertandingan selesai ---"))
        self.stdout.write(
            self.style.SUCCESS("\n--- Populasi data selesai sepenuhnya! ---")
        )
        self.stdout.write(self.style.SUCCESS(f"Total tim: {len(all_teams)}"))
        self.stdout.write(
            self.style.SUCCESS(
                f"Grup A: {len([t for t in all_teams if team_groups.get(t) == 'A'])} tim"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Grup B: {len([t for t in all_teams if team_groups.get(t) == 'B'])} tim"
            )
        )
