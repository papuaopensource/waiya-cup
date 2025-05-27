from django.views.generic import TemplateView
from django.utils.html import format_html
import datetime  # Import for match date/time


class HomeListView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # SVG Definitions (as functions for clarity, could be static strings)
        def get_win_svg():
            return '<svg xmlns="http://www.w3.org/2000/svg" class="shrink-0 size-5 text-emerald-100 bg-emerald-500 rounded-full" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="m9 12l2 2l4-4"></path></g></svg>'

        def get_loss_svg():
            return '<svg xmlns="http://www.w3.org/2000/svg" class="shrink-0 size-5 text-red-100 bg-red-500 rounded-full" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="m15 9l-6 6m0-6l6 6"></path></g></svg>'

        def get_draw_svg():
            return '<svg xmlns="http://www.w3.org/2000/svg" class="shrink-0 size-5 text-gray-100 bg-gray-400 rounded-full" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M8 12h8"></path></g></svg>'

        def get_placeholder_svg():
            return '<svg xmlns="http://www.w3.org/2000/svg" class="shrink-0 size-5 text-gray-100 bg-gray-200 rounded-full" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="#e7e5e4" opacity="0.3"/><path fill="#e7e5e4" d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10s10-4.47 10-10S17.53 2 12 2m0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8s8 3.58 8 8s-3.58 8-8 8"/></svg>'

        # Helper function to generate the list of SVG strings for last 5 matches
        def render_last5_icons_html(last5_results):
            icons_html = []
            for result in last5_results:
                if result == "W":
                    icons_html.append(get_win_svg())
                elif result == "L":
                    icons_html.append(get_loss_svg())
                elif result == "D":
                    icons_html.append(get_draw_svg())
                # If there's an empty string or unrecognized result, it won't add an icon here

            # Fill remaining slots with placeholders up to 5
            while len(icons_html) < 5:
                icons_html.append(get_placeholder_svg())

            # Join all SVG strings into a single HTML string
            return format_html("".join(icons_html))

        # Determine the active tab from URL parameter
        # Default to 'matches' if no tab or an invalid tab is specified
        active_tab = self.request.GET.get("tab", "matches")
        if active_tab not in ["matches", "standings", "statistics"]:
            active_tab = "matches"  # Fallback to default

        context["active_tab"] = active_tab

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
                        },
                        {
                            "name": "Persebu FC",
                            "village": "Kampung Persebu",
                            "mp": 4,
                            "w": 2,
                            "d": 1,
                            "l": 1,
                            "gf": 6,
                            "ga": 5,
                            "gd": 1,
                            "pts": 7,
                            "last5": ["L", "W", "D", "W"],
                        },
                        {
                            "name": "Porambu FC",
                            "village": "Kampung Porambu",
                            "mp": 4,
                            "w": 2,
                            "d": 0,
                            "l": 2,
                            "gf": 7,
                            "ga": 6,
                            "gd": 1,
                            "pts": 6,
                            "last5": ["W", "L", "W", "L"],
                        },
                        {
                            "name": "Swis FC",
                            "village": "Kampung Swis",
                            "mp": 4,
                            "w": 0,
                            "d": 3,
                            "l": 1,
                            "gf": 3,
                            "ga": 5,
                            "gd": -2,
                            "pts": 3,
                            "last5": ["D", "D", "L", "D"],
                        },
                        {
                            "name": "Portas FC",
                            "village": "Kampung Portas",
                            "mp": 4,
                            "w": 0,
                            "d": 0,
                            "l": 4,
                            "gf": 2,
                            "ga": 10,
                            "gd": -8,
                            "pts": 0,
                            "last5": ["L", "L", "L", "L"],
                        },
                        {
                            "name": "Waiya Jr",
                            "village": "Kampung Waiya",
                            "mp": 3,
                            "w": 1,
                            "d": 1,
                            "l": 1,
                            "gf": 3,
                            "ga": 3,
                            "gd": 0,
                            "pts": 4,
                            "last5": ["W", "D", "L"],
                        },
                        {
                            "name": "Bemta FC",
                            "village": "Kampung Bemta",
                            "mp": 3,
                            "w": 0,
                            "d": 2,
                            "l": 1,
                            "gf": 2,
                            "ga": 3,
                            "gd": -1,
                            "pts": 2,
                            "last5": ["D", "L", "D"],
                        },
                        {
                            "name": "PSK Kendate",
                            "village": "Kampung Kendate",
                            "mp": 3,
                            "w": 1,
                            "d": 0,
                            "l": 2,
                            "gf": 4,
                            "ga": 5,
                            "gd": -1,
                            "pts": 3,
                            "last5": ["L", "W", "L"],
                        },
                        {
                            "name": "Arema FC",
                            "village": "Kampung Arema",
                            "mp": 3,
                            "w": 2,
                            "d": 1,
                            "l": 0,
                            "gf": 7,
                            "ga": 2,
                            "gd": 5,
                            "pts": 7,
                            "last5": ["W", "D", "W"],
                        },
                        {
                            "name": "Dobukurung FC",
                            "village": "Kampung Dobukurung",
                            "mp": 3,
                            "w": 1,
                            "d": 0,
                            "l": 2,
                            "gf": 3,
                            "ga": 5,
                            "gd": -2,
                            "pts": 3,
                            "last5": ["L", "L", "W"],
                        },
                        {
                            "name": "PAS Demoi",
                            "village": "Kampung Demoi",
                            "mp": 3,
                            "w": 0,
                            "d": 1,
                            "l": 2,
                            "gf": 1,
                            "ga": 4,
                            "gd": -3,
                            "pts": 1,
                            "last5": ["D", "L", "L"],
                        },
                        {
                            "name": "Pase Putra",
                            "village": "Kampung Pase",
                            "mp": 3,
                            "w": 2,
                            "d": 0,
                            "l": 1,
                            "gf": 5,
                            "ga": 3,
                            "gd": 2,
                            "pts": 6,
                            "last5": ["W", "W", "L"],
                        },
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
                        },
                        {
                            "name": "Setan Merah",
                            "village": "Kampung Setan Merah",
                            "mp": 4,
                            "w": 2,
                            "d": 1,
                            "l": 1,
                            "gf": 7,
                            "ga": 4,
                            "gd": 3,
                            "pts": 7,
                            "last5": ["W", "L", "W", "D"],
                        },
                        {
                            "name": "Red wine Jr",
                            "village": "Kampung Red Wine",
                            "mp": 4,
                            "w": 1,
                            "d": 2,
                            "l": 1,
                            "gf": 5,
                            "ga": 5,
                            "gd": 0,
                            "pts": 5,
                            "last5": ["D", "W", "L", "D"],
                        },
                        {
                            "name": "Waiya Putra",
                            "village": "Kampung Waiya",
                            "mp": 4,
                            "w": 1,
                            "d": 1,
                            "l": 2,
                            "gf": 4,
                            "ga": 6,
                            "gd": -2,
                            "pts": 4,
                            "last5": ["L", "D", "W", "L"],
                        },
                        {
                            "name": "Sokisi Putra",
                            "village": "Kampung Sokisi",
                            "mp": 4,
                            "w": 0,
                            "d": 3,
                            "l": 1,
                            "gf": 3,
                            "ga": 4,
                            "gd": -1,
                            "pts": 3,
                            "last5": ["D", "D", "L", "D"],
                        },
                        {
                            "name": "Star Seroyena",
                            "village": "Kampung Seroyena",
                            "mp": 3,
                            "w": 2,
                            "d": 0,
                            "l": 1,
                            "gf": 6,
                            "ga": 3,
                            "gd": 3,
                            "pts": 6,
                            "last5": ["W", "L", "W"],
                        },
                        {
                            "name": "Sebics FC",
                            "village": "Kampung Sebics",
                            "mp": 3,
                            "w": 1,
                            "d": 1,
                            "l": 1,
                            "gf": 4,
                            "ga": 4,
                            "gd": 0,
                            "pts": 4,
                            "last5": ["D", "W", "L"],
                        },
                        {
                            "name": "Kerikil Putra",
                            "village": "Kampung Kerikil",
                            "mp": 3,
                            "w": 0,
                            "d": 1,
                            "l": 2,
                            "gf": 2,
                            "ga": 5,
                            "gd": -3,
                            "pts": 1,
                            "last5": ["L", "D", "L"],
                        },
                        {
                            "name": "Bambar Jr",
                            "village": "Kampung Bambar",
                            "mp": 3,
                            "w": 2,
                            "d": 0,
                            "l": 1,
                            "gf": 5,
                            "ga": 2,
                            "gd": 3,
                            "pts": 6,
                            "last5": ["W", "W", "L"],
                        },
                        {
                            "name": "Tanah Merah FC",
                            "village": "Kampung Tanah Merah",
                            "mp": 3,
                            "w": 1,
                            "d": 1,
                            "l": 1,
                            "gf": 3,
                            "ga": 3,
                            "gd": 0,
                            "pts": 4,
                            "last5": ["D", "L", "W"],
                        },
                        {
                            "name": "PS Pasti",
                            "village": "Kampung Pasti",
                            "mp": 3,
                            "w": 0,
                            "d": 0,
                            "l": 3,
                            "gf": 1,
                            "ga": 6,
                            "gd": -5,
                            "pts": 0,
                            "last5": ["L", "L", "L"],
                        },
                        {
                            "name": "Wasa FC",
                            "village": "Kampung Wasa",
                            "mp": 3,
                            "w": 1,
                            "d": 0,
                            "l": 2,
                            "gf": 3,
                            "ga": 4,
                            "gd": -1,
                            "pts": 3,
                            "last5": ["L", "W", "L"],
                        },
                    ],
                },
            ]

            # Function to sort teams
            def sort_teams(teams):
                return sorted(
                    teams, key=lambda x: (-x["pts"], -x["gd"], -x["gf"], x["name"])
                )

            # Process data: sort teams and generate last5_html
            for group in all_group_data:
                group["teams"] = sort_teams(group["teams"])
                for team in group["teams"]:
                    team["last5_html"] = render_last5_icons_html(team["last5"])

            context["group_data"] = all_group_data
        # --- Data for 'Matches' (Pertandingan) Tab ---
        elif active_tab == "matches":
            context["matches_data"] = [
                {
                    "date": datetime.date(2025, 5, 27),
                    "time": "14:00",
                    "team1": "Kalsor FC",
                    "team2": "Mamba FC",
                    "score1": 2,
                    "score2": 1,
                    "group": "Grup A",
                    "status": "Finished",
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
                },
                {
                    "date": datetime.date(2025, 5, 28),
                    "time": "14:00",
                    "team1": "Persada FC",
                    "team2": "Rajawali FC",
                    "score1": None,  # For upcoming matches
                    "score2": None,
                    "group": "Grup A",
                    "status": "Upcoming",
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
                },
            ]

        # --- Data for 'Statistics' (Statistik) Tab ---
        elif active_tab == "statistics":
            context["statistics_data"] = {
                "top_scorers": [
                    {"name": "Pemain A", "club": "Kalsor FC", "goals": 5},
                    {"name": "Pemain B", "club": "Astor FC", "goals": 4},
                    {"name": "Pemain C", "club": "Mamba FC", "goals": 3},
                ],
                "most_assists": [
                    {"name": "Pemain X", "club": "Bintang FC", "assists": 3},
                    {"name": "Pemain Y", "club": "Kalsor FC", "assists": 2},
                ],
                "clean_sheets": [
                    {"name": "Kiper P", "club": "Astor FC", "clean_sheets": 2},
                    {"name": "Kiper Q", "club": "Mamba FC", "clean_sheets": 1},
                ],
            }

        return context
