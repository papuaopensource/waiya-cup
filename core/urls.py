# football_app/urls.py (or your project's main urls.py if not within an app)
from django.urls import path
from .views import (
    HomeListView,
    ContributeDataView,
    ContributeDataSuccessView,
)  # We will create these views

app_name = "core"  # Define the app namespace for URL namespacing
urlpatterns = [
    path("", HomeListView.as_view(), name="index"),  # Default home page shows matches
    # --- URL untuk Kontribusi Data (sudah ada dan tidak perlu diubah) ---
    path("kontribusi/data/", ContributeDataView.as_view(), name="contribute_data_form"),
    path(
        "kontribusi/data/sukses/",
        ContributeDataSuccessView.as_view(),
        name="contribute_data_success",
    ),
    # --- Akhir ---
]
