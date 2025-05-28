# football_app/forms.py
from django import forms
from .models import DataContribution, Match

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
        required=True,
        label=DataContribution._meta.get_field(
            "match_to_update"
        ).verbose_name,  # Mengambil verbose_name dari model
        empty_label="-- Pilih Pertandingan --",
        widget=forms.Select(attrs=SELECT_ATTRS),
    )
    new_score1 = forms.IntegerField(
        required=True,
        label=DataContribution._meta.get_field("new_score1").verbose_name,
        min_value=0,
        widget=forms.NumberInput(attrs={**COMMON_ATTRS, "placeholder": "Skor Tim 1"}),
    )
    new_score2 = forms.IntegerField(
        required=True,
        label=DataContribution._meta.get_field("new_score2").verbose_name,
        min_value=0,
        widget=forms.NumberInput(attrs={**COMMON_ATTRS, "placeholder": "Skor Tim 2"}),
    )

    # PERUBAHAN DI SINI: placeholder/help_text untuk description
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                **TEXTAREA_ATTRS,
                "placeholder": "Masukkan deskripsi kontribusi Anda di sini...",
            }
        ),
        required=False,
        label=DataContribution._meta.get_field("description").verbose_name,
        help_text=DataContribution._meta.get_field(
            "description"
        ).help_text,  # Mengambil help_text dari model
    )
    contributor_name = forms.CharField(
        max_length=100,
        required=False,
        label=DataContribution._meta.get_field("contributor_name").verbose_name,
        widget=forms.TextInput(
            attrs={**COMMON_ATTRS, "placeholder": "Contoh: Theis Andatu"}
        ),
    )

    class Meta:
        model = DataContribution
        fields = [
            "match_to_update",
            "new_score1",
            "new_score2",
            "description",
            "contributor_name",
        ]

    def clean(self):
        cleaned_data = super().clean()

        match_selected = cleaned_data.get("match_to_update")
        new_score1 = cleaned_data.get("new_score1")
        new_score2 = cleaned_data.get("new_score2")

        # Validasi sederhana
        if match_selected and (new_score1 is None or new_score2 is None):
            if new_score1 is None:
                self.add_error("new_score1", "Skor tim kandang wajib diisi.")
            if new_score2 is None:
                self.add_error("new_score2", "Skor tim tandang wajib diisi.")

        # contribution_type otomatis dari model, tidak perlu diatur di sini
        # cleaned_data['contribution_type'] = 'match_result'

        return cleaned_data
