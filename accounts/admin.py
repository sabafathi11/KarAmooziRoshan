from django.contrib import admin
from .models import User, ActivityLog, Report

admin.site.register(User)
admin.site.register(ActivityLog)
admin.site.register(Report)
