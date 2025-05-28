# football_app/views.py
from django.views.generic import TemplateView, FormView
from datetime import date, timedelta
from collections import defaultdict
from .models import Team, Player, Match, models
from django.urls import reverse_lazy
from .forms import DataContributionForm  # Import form yang baru dibuat

import random


class ContributeDataView(FormView):
    template_name = "core/contribute_data_form.html"
    form_class = DataContributionForm
    success_url = reverse_lazy("core:contribute_data_success")

    def get_initial(self):
        initial = super().get_initial()
        if self.request.method == "POST" and "contribution_type" in self.request.POST:
            initial["contribution_type"] = self.request.POST["contribution_type"]
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST":
            kwargs["data"] = self.request.POST
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Kontribusi Data"

        if "form" in kwargs:
            current_form = kwargs["form"]
        elif self.request.method == "POST":
            current_form = self.get_form()
        else:
            current_form = self.get_form()

        context["selected_contribution_type"] = current_form.data.get(
            "contribution_type", current_form.initial.get("contribution_type", "")
        )

        return context


class ContributeDataSuccessView(TemplateView):
    template_name = "core/contribute_data_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Terima Kasih!"
        return context


class HomeListView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Tentukan tab aktif dari parameter URL, default ke 'matches'
        active_tab = self.request.GET.get("tab", "matches")
        if active_tab not in ["matches", "standings", "statistics"]:
            active_tab = "matches"
        context["active_tab"] = active_tab

        # --- Data untuk Tab 'Matches' (Pertandingan) ---
        if active_tab == "matches":
            # Ambil semua data pertandingan, pilih nama tim terkait secara efisien
            all_matches_data = (
                Match.objects.all()
                .select_related("team1", "team2")
                .values(
                    "date",
                    "time",
                    "team1__name",
                    "team2__name",
                    "score1",
                    "score2",
                    "group",
                    "status",
                    "matchday",
                )
            )

            # Konversi QuerySet ke list of dicts untuk manipulasi lebih mudah
            all_matches_list = list(all_matches_data)

            # Dapatkan matchday unik dari semua pertandingan yang tersedia
            unique_matchdays = sorted(
                list(set(m["matchday"] for m in all_matches_list))
            )
            matchday_options = [
                {"label": f"Matchday {md}", "value": str(md)} for md in unique_matchdays
            ]

            # Tentukan matchday awal yang akan ditampilkan (terbaru atau dipilih dari URL)
            initial_display_matchday = None
            if unique_matchdays:
                if self.request.GET.get("matchday"):
                    try:
                        selected_matchday_int = int(self.request.GET["matchday"])
                        if selected_matchday_int in unique_matchdays:
                            initial_display_matchday = str(selected_matchday_int)
                        else:
                            initial_display_matchday = str(
                                unique_matchdays[-1]
                            )  # Fallback ke matchday terbaru
                    except ValueError:
                        initial_display_matchday = str(
                            unique_matchdays[-1]
                        )  # Fallback ke matchday terbaru
                else:
                    initial_display_matchday = str(
                        unique_matchdays[-1]
                    )  # Default ke matchday terbaru jika tanpa parameter

            # Filter pertandingan berdasarkan matchday yang ditentukan
            matches_to_display = []
            if initial_display_matchday:
                matches_to_display = [
                    {
                        "date": match["date"],
                        "time": match["time"],
                        "team1": match["team1__name"],
                        "team2": match["team2__name"],
                        "score1": match["score1"],
                        "score2": match["score2"],
                        "group": match["group"],
                        "status": match["status"],
                        "matchday": match["matchday"],
                    }
                    for match in all_matches_list
                    if str(match["matchday"]) == initial_display_matchday
                ]

            context["matches_data"] = matches_to_display
            context["matchday_options"] = matchday_options
            context["initial_display_matchday"] = initial_display_matchday

        # --- Data untuk Tab 'Standings' (Klasemen) ---
        elif active_tab == "standings":
            # Ambil tim yang telah berpartisipasi dalam setidaknya satu pertandingan
            participating_teams = Team.objects.filter(
                models.Q(home_matches__isnull=False)
                | models.Q(away_matches__isnull=False)
            ).distinct()

            standings_by_group = defaultdict(lambda: {})

            # Proses pertandingan yang sudah selesai, diurutkan berdasarkan tanggal dan waktu untuk 'last5' yang benar
            finished_matches = (
                Match.objects.filter(status="Finished")
                .select_related("team1", "team2")
                .order_by("date", "time")
            )

            for match in finished_matches:
                group_name = match.group

                # Inisialisasi statistik tim jika belum ada dalam grup
                if match.team1.name not in standings_by_group[group_name]:
                    standings_by_group[group_name][match.team1.name] = {
                        "name": match.team1.name,
                        "village": match.team1.village,
                        "mp": 0,
                        "w": 0,
                        "d": 0,
                        "l": 0,
                        "gf": 0,
                        "ga": 0,
                        "gd": 0,
                        "pts": 0,
                        "last5": [],
                    }
                if match.team2.name not in standings_by_group[group_name]:
                    standings_by_group[group_name][match.team2.name] = {
                        "name": match.team2.name,
                        "village": match.team2.village,
                        "mp": 0,
                        "w": 0,
                        "d": 0,
                        "l": 0,
                        "gf": 0,
                        "ga": 0,
                        "gd": 0,
                        "pts": 0,
                        "last5": [],
                    }

                team1_stats = standings_by_group[group_name][match.team1.name]
                team2_stats = standings_by_group[group_name][match.team2.name]

                # Perbarui Matches Played
                team1_stats["mp"] += 1
                team2_stats["mp"] += 1

                # Perbarui Goals For and Against
                team1_stats["gf"] += match.score1
                team1_stats["ga"] += match.score2
                team2_stats["gf"] += match.score2
                team2_stats["ga"] += match.score1

                # Perbarui Wins, Draws, Losses dan Points, serta hasil 'last5'
                team1_result = ""
                team2_result = ""

                if match.score1 > match.score2:
                    team1_stats["w"] += 1
                    team2_stats["l"] += 1
                    team1_stats["pts"] += 3
                    team1_result = "W"
                    team2_result = "L"
                elif match.score2 > match.score1:
                    team2_stats["w"] += 1
                    team1_stats["l"] += 1
                    team2_stats["pts"] += 3
                    team2_result = "W"
                    team1_result = "L"
                else:  # Draw
                    team1_stats["d"] += 1
                    team2_stats["d"] += 1
                    team1_stats["pts"] += 1
                    team2_stats["pts"] += 1
                    team1_result = "D"
                    team2_result = "D"

                # Perbarui Goal Difference
                team1_stats["gd"] = team1_stats["gf"] - team1_stats["ga"]
                team2_stats["gd"] = team2_stats["gf"] - team2_stats["ga"]

                # --- Perbarui Hasil 5 Terakhir ---
                team1_stats["last5"].append(team1_result)
                team2_stats["last5"].append(team2_result)

                if len(team1_stats["last5"]) > 5:
                    team1_stats["last5"].pop(0)
                if len(team2_stats["last5"]) > 5:
                    team2_stats["last5"].pop(0)

            # Konversi defaultdict ke list of dicts untuk template
            all_group_data = []
            for group_key in sorted(standings_by_group.keys()):
                teams_in_group = standings_by_group[group_key].values()
                sorted_teams = sorted(
                    teams_in_group,
                    key=lambda x: (-x["pts"], -x["gd"], -x["gf"], x["name"]),
                )
                all_group_data.append(
                    {"name": f"Grup {group_key}", "teams": sorted_teams}
                )

            context["group_data"] = all_group_data

        # --- Data untuk Tab 'Statistics' (Statistik) ---
        elif active_tab == "statistics":
            # Ambil semua pemain dan data tim terkait mereka
            all_players = Player.objects.all().select_related("team")

            # Top Scorers: Filter pemain dengan gol, urutkan, dan format untuk template
            top_scorers = sorted(
                [p for p in all_players if p.goals > 0],
                key=lambda x: (-x.goals, x.name),
            )[:10]

            # Most Assists: Filter pemain dengan assist, urutkan, dan format
            most_assists = sorted(
                [p for p in all_players if p.assists > 0],
                key=lambda x: (-x.assists, x.name),
            )[:10]

            # Goals + Assists: Gunakan @property 'total_goals_assists' dari model Player
            goals_plus_assists = sorted(
                [p for p in all_players if p.total_goals_assists > 0],
                key=lambda x: (-x.total_goals_assists, x.name),
            )[:10]

            context["statistics_data"] = {
                "top_scorers": [
                    {"name": p.name, "club": p.team.name, "goals": p.goals}
                    for p in top_scorers
                ],
                "most_assists": [
                    {"name": p.name, "club": p.team.name, "assists": p.assists}
                    for p in most_assists
                ],
                "goals_plus_assists": [
                    {
                        "name": p.name,
                        "club": p.team.name,
                        "total_g_a": p.total_goals_assists,
                    }
                    for p in goals_plus_assists
                ],
            }

        return context
