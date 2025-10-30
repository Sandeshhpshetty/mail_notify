from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls")),
    # optional root redirect to register
    path("", RedirectView.as_view(url="/register/", permanent=False)),
]
