from django.contrib import admin
from .models import Dataset, Text, Label

admin.site.register(Dataset)
admin.site.register(Text)
admin.site.register(Label)