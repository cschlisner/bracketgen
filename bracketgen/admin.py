from django.contrib import admin
from .models import Tournament, Player, Round, Match

# Register your models here.

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
	list_display = ('name', 'reference_code', 'status', 'user_owner')
	list_filter = ('name', 'reference_code', 'status', 'user_owner')
    
@admin.register(Player)
class TournamentAdmin(admin.ModelAdmin):
	list_display = ('name', 'wins', 'losses', 'match')
	list_filter = ('name', 'wins', 'losses', 'match')
    
# admin.site.register(Tournament)
# admin.site.register(Player)
@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
	list_display = ('name', 'index')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
	list_display = ('name', 'index')