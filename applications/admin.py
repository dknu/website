from django.contrib import admin
from .models import Application, ProjectApplication

class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'group_choice',
    ]

admin.site.register(Application, ApplicationAdmin)

class ProjectApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'email',
    ]

admin.site.register(ProjectApplication, ProjectApplicationAdmin)
