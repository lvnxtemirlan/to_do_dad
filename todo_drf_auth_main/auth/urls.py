from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("auth.app.urls")),
]
