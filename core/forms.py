# football_app/forms.py
from django import forms
from .models import DataContribution, Team, Player, Match

# Define common Tailwind CSS classes for form widgets (tetap sama)
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

    player_to_update = forms.ModelChoiceField(
        queryset=Player.objects.all().select_related("team").order_by("name"),
        required=False,
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
            "player_to_update",
            "goals_added",
            "assists_added",
            # "proposed_team_name", "proposed_team_village", # Dihapus
            "description",
            "contributor_name",
            "contributor_email",
        ]
        labels = {
            "contribution_type": "Jenis Kontribusi",
            "new_score1": "Skor Tim Kandang Baru",
            "new_score2": "Skor Tim Tandang Baru",
            "goals_added": "Jumlah Gol yang Ditambahkan",
            "assists_added": "Jumlah Assist yang Ditambahkan",
            # "proposed_team_name": "Nama Tim Baru yang Diusulkan", # Dihapus
            # "proposed_team_village": "Desa/Wilayah Asal Tim Baru", # Dihapus
            "description": "Deskripsi/Detail Tambahan",
            "contributor_name": "Nama Anda (Opsional)",
            "contributor_email": "Email Anda (Opsional, untuk konfirmasi)",
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
            # "proposed_team_name": forms.TextInput(attrs={**COMMON_ATTRS, 'placeholder': 'Contoh: Garuda Muda FC'}), # Dihapus
            # "proposed_team_village": forms.TextInput(attrs={**COMMON_ATTRS, 'placeholder': 'Contoh: Desa Jaya'}), # Dihapus
            "description": forms.Textarea(
                attrs={
                    **TEXTAREA_ATTRS,
                    "placeholder": "Jelaskan detail kontribusi Anda.",
                }
            ),
            "contributor_name": forms.TextInput(
                attrs={**COMMON_ATTRS, "placeholder": "Contoh: Budi Santoso"}
            ),
            "contributor_email": forms.EmailInput(
                attrs={**COMMON_ATTRS, "placeholder": "contoh@email.com"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        contribution_type = cleaned_data.get("contribution_type")

        # Hapus semua field yang tidak relevan agar tidak mengganggu validasi conditional
        irrelevant_fields = {
            "match_result": [
                "player_to_update",
                "goals_added",
                "assists_added",
            ],  # proposed_team_name, proposed_team_village dihapus
            "player_stats": [
                "match_to_update",
                "new_score1",
                "new_score2",
            ],  # proposed_team_name, proposed_team_village dihapus
            # 'new_team' dan 'other' dihapus
        }

        if contribution_type in irrelevant_fields:
            for field_name in irrelevant_fields[contribution_type]:
                cleaned_data[field_name] = None
                if isinstance(self.fields.get(field_name), forms.CharField):
                    cleaned_data[field_name] = ""
                elif isinstance(self.fields.get(field_name), forms.IntegerField):
                    cleaned_data[field_name] = None

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
                # self.add_error('assists_added', '') # Opsional: untuk menghilangkan error dari field lain

        # Tidak perlu validasi untuk 'new_team' atau 'other' lagi

        # Untuk 'description', kita tidak perlu mewajibkan jika sudah ada field spesifik yang diisi
        # Tapi jika Anda ingin description selalu ada, Anda bisa tambahkan validasi ini:
        # if not cleaned_data.get('description'):
        #     self.add_error('description', 'Deskripsi kontribusi wajib diisi.')

        return cleaned_data
