# football_app/urls.py (or your project's main urls.py if not within an app)
from django.urls import path
from .views import HomeListView  # We will create these views

app_name = "core"  # Define the app namespace for URL namespacing
urlpatterns = [
    path("", HomeListView.as_view(), name="index"),  # Default home page shows matches
]
