from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

# Local
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", views.UserView.as_view({"get": "list"}), name="user-list"),
    path("login/", views.LoginView.as_view({"post": "create"}), name="login"),
    path(
        "refresh/", views.RefreshTokenView.as_view({"post": "create"}), name="refresh"
    ),
    path("verify/", views.VerifyView.as_view({"post": "verify"}), name="token_verify"),
    path(
        "password/change/",
        views.PasswordView.as_view({"post": "change"}),
        name="change_password",
    ),
    path("skills/", views.SkillView.as_view({"get": "get_skills",
                                             "post": "create_skill"}), name="skills"),
    path("work/", views.WorkView.as_view({"get": "get_skills"}), name="get_work"),
    path("edu/", views.EducationView.as_view({"get": "get_skills"}), name="get_edu"),

]

router = DefaultRouter()

router.register("register", views.RegisterView, basename="register")


urlpatterns += router.urls
