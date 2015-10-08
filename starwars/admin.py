from __future__ import unicode_literals

from django.contrib import admin

from .models import (
    People,
    Planet,
    Film,
    Starship,
    Vehicle,
    Species

)

classes = [People, Planet, Film, Starship, Vehicle, Species]


class ModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        return False

for c in classes:
    admin.site.register(c, ModelAdmin)
