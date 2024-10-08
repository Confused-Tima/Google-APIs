from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls", namespace="main")),
    path("", include("users.urls", namespace="users")),
]

if settings.DEBUG:
    print("=--->>Running in Debug and loading static url")
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )  # type: ignore
else:
    print("Not Running in Debug")
