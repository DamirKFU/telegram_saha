from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        "api-test/",
        include(("api.urls")),
        name="apit-test",
    ),
    path("", admin.site.urls),
]
