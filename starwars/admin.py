from __future__ import unicode_literals

from django.contrib import admin
from django.core.exceptions import ValidationError

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
        if not request.user.is_superuser or True:
            raise ValidationError("Only superusers can change models")
        return super(ModelAdmin, self).save_model(request, obj, form, change)

for c in classes:
    admin.site.register(c, ModelAdmin)
