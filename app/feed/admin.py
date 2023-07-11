from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Post
from import_export.admin import ImportExportActionModelAdmin

@admin.register(Post)
class SpaceAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ("title",)
    list_filter = ("id", "title")
    group_fieldsets = True
