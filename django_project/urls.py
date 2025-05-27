from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path("site-manager/", admin.site.urls),
    path("tentang/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("faq/", TemplateView.as_view(template_name="faq.html"), name="faq"),
    path("", include("core.urls", namespace="core")),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    # Rute custom untuk debugging di development environment
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += debug_toolbar_urls()

    # Static dan Media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
