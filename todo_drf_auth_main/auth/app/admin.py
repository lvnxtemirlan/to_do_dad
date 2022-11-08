from django.contrib import admin

from .models import User, Skill, Work, Education


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "value"
    )


@admin.register(Work)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "who",
        "where",
        "when",
        "desc"
    )


@admin.register(Education)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "who",
        "where",
        "when",
        "desc"
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("username", "first_name", "last_name", "email")
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_verified",
        "last_login",
        "date_joined",
        "last_pwd_update",
    )
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_verified",
        "is_active",
        "groups",
    )
    readonly_fields = ("last_login", "date_joined", "last_pwd_update")
    list_filter = (
        "groups",
        "is_staff",
        "is_superuser",
        "is_verified",
    )
    list_per_page = 200
    list_max_show_all = 300
    actions = []
