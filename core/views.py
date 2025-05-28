from django.views.generic import TemplateView
import datetime


class HomeListView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Determine the active tab from URL parameter
        # Default to 'matches' if no tab or an invalid tab is specified
        active_tab = self.request.GET.get("tab", "matches")
        if active_tab not in ["matches", "standings", "statistics"]:
            active_tab = "matches"  # Fallback to default

        context["active_tab"] = active_tab

        # Get the selected matchday from the URL parameter
        selected_matchday_param = self.request.GET.get("matchday")

        # --- Data for 'Standings' (Klasemen) Tab ---
        if active_tab == "standings":
            all_group_data = [
                {
                    "name": "Grup A",
                    "teams": [
                        {
                            "name": "Kalsor FC",
                            "village": "Kampung Kalsor",
                            "mp": 4,
                            "w": 3,
                            "d": 1,
                            "l": 0,
                            "gf": 8,
                            "ga": 4,
                            "gd": 4,
                            "pts": 10,
                            "last5": ["W", "D", "W", "W"],
                        }
                    ],
                },
                {
                    "name": "Grup B",
                    "teams": [
                        {
                            "name": "Astor FC",
                            "village": "Kampung Astor",
                            "mp": 4,
                            "w": 3,
                            "d": 1,
                            "l": 0,
                            "gf": 9,
                            "ga": 3,
                            "gd": 6,
                            "pts": 10,
                            "last5": ["W", "W", "D", "W"],
                        }
                    ],
                },
            ]

            # Function to sort teams
            def sort_teams(teams):
                return sorted(
                    teams, key=lambda x: (-x["pts"], -x["gd"], -x["gf"], x["name"])
                )

            # Process data: sort teams (no need to generate HTML here)
            for group in all_group_data:
                group["teams"] = sort_teams(group["teams"])

            context["group_data"] = all_group_data

        # --- Data for 'Matches' (Pertandingan) Tab ---
        elif active_tab == "matches":
            all_matches_data = [
                {
                    "date": datetime.date(2025, 5, 27),
                    "time": "14:00",
                    "team1": "Kalsor FC",
                    "team2": "Mamba FC",
                    "score1": 2,
                    "score2": 1,
                    "group": "Grup A",
                    "status": "Finished",
                    "matchday": 1,
                },
                {
                    "date": datetime.date(2025, 5, 27),
                    "time": "16:00",
                    "team1": "Astor FC",
                    "team2": "Bintang FC",
                    "score1": 3,
                    "score2": 0,
                    "group": "Grup B",
                    "status": "Finished",
                    "matchday": 1,
                },
                {
                    "date": datetime.date(2025, 5, 28),
                    "time": "14:00",
                    "team1": "Persada FC",
                    "team2": "Rajawali FC",
                    "score1": None,
                    "score2": None,
                    "group": "Grup A",
                    "status": "Upcoming",
                    "matchday": 2,
                },
                {
                    "date": datetime.date(2025, 5, 28),
                    "time": "16:00",
                    "team1": "Garuda FC",
                    "team2": "Elang FC",
                    "score1": None,
                    "score2": None,
                    "group": "Grup B",
                    "status": "Upcoming",
                    "matchday": 2,
                },
                {
                    "date": datetime.date(2025, 5, 29),
                    "time": "14:00",
                    "team1": "Another FC",
                    "team2": "Yet Another FC",
                    "score1": None,
                    "score2": None,
                    "group": "Grup C",
                    "status": "Upcoming",
                    "matchday": 3,
                },
            ]

            # Generate options for the matchday dropdown
            unique_matchdays = sorted(
                list(set(m["matchday"] for m in all_matches_data))
            )
            matchday_options = [
                {"label": f"Matchday {md}", "value": str(md)}
                for md in unique_matchdays  # Ensure value is string
            ]

            # Determine the initial matchday to display
            # If a matchday is selected in the URL, use it.
            # Otherwise, default to the latest matchday.
            if selected_matchday_param:
                try:
                    selected_matchday_int = int(selected_matchday_param)
                    # Ensure the selected matchday is valid
                    if selected_matchday_int in unique_matchdays:
                        initial_display_matchday = selected_matchday_param
                    else:
                        # Fallback to the latest if invalid param
                        initial_display_matchday = (
                            str(unique_matchdays[-1]) if unique_matchdays else ""
                        )
                except ValueError:
                    # Fallback to the latest if param is not an integer
                    initial_display_matchday = (
                        str(unique_matchdays[-1]) if unique_matchdays else ""
                    )
            else:
                # Default to the latest matchday if no param
                initial_display_matchday = (
                    str(unique_matchdays[-1]) if unique_matchdays else ""
                )

            # Filter matches based on the determined display matchday
            if initial_display_matchday:
                matches_data = [
                    m
                    for m in all_matches_data
                    if str(m["matchday"]) == initial_display_matchday
                ]
            else:
                matches_data = []  # No matches if no matchdays are defined

            context["matches_data"] = matches_data
            context["matchday_options"] = matchday_options
            context["initial_display_matchday"] = (
                initial_display_matchday  # New context variable
            )

        # --- Data for 'Statistics' (Statistik) Tab ---
        elif active_tab == "statistics":
            # Example data for top scorers and assists.
            # In a real application, this would likely come from a database.
            top_scorers_raw = [
                {"name": "Pemain A", "club": "Kalsor FC", "goals": 5},
                {"name": "Pemain B", "club": "Astor FC", "goals": 4},
                {"name": "Pemain C", "club": "Mamba FC", "goals": 3},
                {"name": "Pemain D", "club": "Bintang FC", "goals": 3},
                {"name": "Pemain E", "club": "Kalsor FC", "goals": 2},
            ]
            most_assists_raw = [
                {"name": "Pemain X", "club": "Bintang FC", "assists": 3},
                {"name": "Pemain Y", "club": "Kalsor FC", "assists": 2},
                {"name": "Pemain Z", "club": "Astor FC", "assists": 2},
                {
                    "name": "Pemain A",
                    "club": "Kalsor FC",
                    "assists": 1,
                },  # Pemain A juga punya assist
            ]

            # Calculate Goals + Assists
            player_stats = {}
            for scorer in top_scorers_raw:
                player_stats[scorer["name"]] = {
                    "club": scorer["club"],
                    "goals": scorer["goals"],
                    "assists": 0,  # Initialize assists
                    "total_g_a": scorer["goals"],  # Initialize total
                }

            for assister in most_assists_raw:
                if assister["name"] in player_stats:
                    player_stats[assister["name"]]["assists"] = assister["assists"]
                    player_stats[assister["name"]]["total_g_a"] += assister["assists"]
                else:
                    # Handle players who only have assists but no goals in top_scorers_raw
                    player_stats[assister["name"]] = {
                        "club": assister["club"],
                        "goals": 0,  # Initialize goals
                        "assists": assister["assists"],
                        "total_g_a": assister["assists"],
                    }

            goals_plus_assists = sorted(
                [
                    {
                        "name": name,
                        "club": stats["club"],
                        "total_g_a": stats["total_g_a"],
                    }
                    for name, stats in player_stats.items()
                ],
                key=lambda x: (
                    -x["total_g_a"],
                    x["name"],
                ),  # Sort by total_g_a (desc), then name (asc)
            )

            context["statistics_data"] = {
                "top_scorers": sorted(
                    top_scorers_raw, key=lambda x: (-x["goals"], x["name"])
                ),
                "most_assists": sorted(
                    most_assists_raw, key=lambda x: (-x["assists"], x["name"])
                ),
                "goals_plus_assists": goals_plus_assists,  # New data for Goals + Assists
                # "clean_sheets": [ # Removed as per request
                #     {"name": "Kiper P", "club": "Astor FC", "clean_sheets": 2},
                #     {"name": "Kiper Q", "club": "Mamba FC", "clean_sheets": 1},
                # ],
            }

        return context
