from django.contrib import admin

from football_app.models import Player, GameRegistration


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass

@admin.register(GameRegistration)
class GameRegistrationAdmin(admin.ModelAdmin):
    pass

