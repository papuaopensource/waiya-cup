# football_app/forms.py
from django import forms
from .models import DataContribution, Team, Player, Match

# Define common Tailwind CSS classes for form widgets
COMMON_ATTRS = {
    "class": "block w-full rounded-md border-gray-300 shadow-sm "
    "focus:border-red-500 focus:ring-red-500 sm:text-sm"
}
SELECT_ATTRS = {
    "class": "block appearance-none w-full bg-white border border-gray-300 text-gray-700 py-2 px-3 pr-8 rounded leading-tight "
    "focus:outline-none focus:bg-white focus:border-red-500 focus:ring-red-500 sm:text-sm"
}
TEXTAREA_ATTRS = {
    "class": "block w-full rounded-md border-gray-300 shadow-sm "
    "focus:border-red-500 focus:ring-red-500 sm:text-sm",
    "rows": 4,
}


class DataContributionForm(forms.ModelForm):
    match_to_update = forms.ModelChoiceField(
        queryset=Match.objects.filter(status="Upcoming")
        .select_related("team1", "team2")
        .order_by("date", "time"),
        required=False,
        label="Pilih Pertandingan",
        empty_label="-- Pilih Pertandingan --",
        widget=forms.Select(attrs=SELECT_ATTRS),
    )

    # NEW FIELD: Untuk memilih tim sebelum memilih pemain
    team_for_player_stats = forms.ModelChoiceField(
        queryset=Team.objects.all().order_by("name"),
        required=False,  # Ini akan wajib di-validasi di clean() jika contribution_type = player_stats
        label="Pilih Tim",
        empty_label="-- Pilih Tim --",
        # Tambahkan onchange untuk submit form lagi
        widget=forms.Select(attrs={**SELECT_ATTRS, "onchange": "this.form.submit();"}),
    )

    player_to_update = forms.ModelChoiceField(
        queryset=Player.objects.none(),  # Default kosong, akan diisi dinamis
        required=False,  # Ini akan wajib di-validasi di clean() jika contribution_type = player_stats
        label="Pilih Pemain",
        empty_label="-- Pilih Pemain --",
        widget=forms.Select(attrs=SELECT_ATTRS),
    )

    class Meta:
        model = DataContribution
        fields = [
            "contribution_type",
            "match_to_update",
            "new_score1",
            "new_score2",
            "team_for_player_stats",  # Tambahkan field baru di sini
            "player_to_update",
            "goals_added",
            "assists_added",
            "description",
            "contributor_name",
        ]
        labels = {
            "contribution_type": "Jenis Kontribusi",
            "new_score1": "Skor Tim Kandang Baru",
            "new_score2": "Skor Tim Tandang Baru",
            "team_for_player_stats": "Pilih Tim untuk Statistik Pemain",  # Label yang lebih spesifik
            "goals_added": "Jumlah Gol yang Ditambahkan",
            "assists_added": "Jumlah Assist yang Ditambahkan",
            "description": "Deskripsi/Detail Tambahan",
            "contributor_name": "Nama Anda",
        }
        widgets = {
            "contribution_type": forms.Select(
                attrs={
                    **SELECT_ATTRS,
                    "id": "id_contribution_type",
                    "onchange": "this.form.submit();",
                }
            ),
            "new_score1": forms.NumberInput(
                attrs={**COMMON_ATTRS, "placeholder": "Skor Tim 1"}
            ),
            "new_score2": forms.NumberInput(
                attrs={**COMMON_ATTRS, "placeholder": "Skor Tim 2"}
            ),
            "goals_added": forms.NumberInput(
                attrs={**COMMON_ATTRS, "placeholder": "Contoh: 1"}
            ),
            "assists_added": forms.NumberInput(
                attrs={**COMMON_ATTRS, "placeholder": "Contoh: 1"}
            ),
            "description": forms.Textarea(
                attrs={
                    **TEXTAREA_ATTRS,
                    "placeholder": "Jelaskan detail kontribusi Anda.",
                }
            ),
            "contributor_name": forms.TextInput(
                attrs={**COMMON_ATTRS, "placeholder": "Contoh: Theis Andatu"}
            ),
        }

    # Constructor method untuk menginisialisasi queryset player_to_update secara dinamis
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Inisialisasi queryset player_to_update
        # Jika form sudah memiliki data POST dan contribution_type adalah 'player_stats'
        # dan team_for_player_stats sudah dipilih
        if self.is_bound and self.data.get("contribution_type") == "player_stats":
            selected_team_id = self.data.get("team_for_player_stats")
            if selected_team_id:
                try:
                    selected_team = Team.objects.get(pk=selected_team_id)
                    self.fields["player_to_update"].queryset = Player.objects.filter(
                        team=selected_team
                    ).order_by("name")
                except Team.DoesNotExist:
                    self.fields["player_to_update"].queryset = Player.objects.none()
            else:
                self.fields["player_to_update"].queryset = Player.objects.none()
        else:
            self.fields["player_to_update"].queryset = (
                Player.objects.none()
            )  # Default kosong

    def clean(self):
        cleaned_data = super().clean()
        contribution_type = cleaned_data.get("contribution_type")

        # Hapus semua field yang tidak relevan agar tidak mengganggu validasi conditional
        irrelevant_fields = {
            "match_result": [
                "team_for_player_stats",
                "player_to_update",
                "goals_added",
                "assists_added",
            ],
            "player_stats": ["match_to_update", "new_score1", "new_score2"],
        }

        if contribution_type in irrelevant_fields:
            for field_name in irrelevant_fields[contribution_type]:
                cleaned_data[field_name] = None
                if isinstance(self.fields.get(field_name), forms.CharField):
                    cleaned_data[field_name] = ""
                elif isinstance(self.fields.get(field_name), forms.IntegerField):
                    cleaned_data[field_name] = None
                elif isinstance(self.fields.get(field_name), forms.ModelChoiceField):
                    cleaned_data[field_name] = None  # Untuk ForeignKey

        # Validasi spesifik berdasarkan tipe kontribusi
        if contribution_type == "match_result":
            if not cleaned_data.get("match_to_update"):
                self.add_error(
                    "match_to_update",
                    "Pilih pertandingan yang ingin Anda laporkan hasilnya.",
                )
            if cleaned_data.get("new_score1") is None:
                self.add_error("new_score1", "Masukkan skor Tim Kandang.")
            if cleaned_data.get("new_score2") is None:
                self.add_error("new_score2", "Masukkan skor Tim Tandang.")

        elif contribution_type == "player_stats":
            # Sekarang, team_for_player_stats harus dipilih dulu
            if not cleaned_data.get("team_for_player_stats"):
                self.add_error("team_for_player_stats", "Pilih tim terlebih dahulu.")
            else:
                # Hanya validasi player_to_update jika tim sudah dipilih
                if not cleaned_data.get("player_to_update"):
                    self.add_error(
                        "player_to_update",
                        "Pilih pemain yang statistiknya ingin Anda laporkan.",
                    )

                if (
                    cleaned_data.get("goals_added") is None
                    or cleaned_data.get("goals_added") == 0
                ) and (
                    cleaned_data.get("assists_added") is None
                    or cleaned_data.get("assists_added") == 0
                ):
                    self.add_error(
                        "goals_added",
                        "Setidaknya masukkan jumlah gol atau assist yang ditambahkan.",
                    )

        return cleaned_data
