from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import Tournament, Player

from django.contrib.auth.models import User

import re

class CreateTournamentForm(forms.Form):
	tournament_name = forms.CharField(required=True, help_text="Enter a name for your tournament", widget=forms.TextInput(attrs={'placeholder': 'name'}))
	tournament_password = forms.CharField(required=False, max_length=50, help_text="Enter an optional tournament password", widget=forms.TextInput(attrs={'placeholder': 'password (optional)'}))

class JoinTournamentForm(forms.Form):
	player_name = forms.CharField(required=True, help_text="Enter a player name", widget=forms.TextInput(attrs={'placeholder': 'player name'}))

class AuthTournamentForm(forms.Form):
	password = forms.CharField(required=True, help_text="Enter the tournament's password", widget=forms.TextInput(attrs={'placeholder': 'password'}))

class GoToTournamentForm(forms.Form):
	reference_code = forms.CharField(required=True, help_text="Enter a tournament code", widget=forms.TextInput(attrs={'placeholder': 'reference code'}))
	def clean_reference_code(self):
		data = self.cleaned_data['reference_code']

		try:
			t = Tournament.objects.get(reference_code = data)
		except Tournament.DoesNotExist:
			raise ValidationError('Tournament does not exist')

		return data

class UpdateUserInfo(forms.Form):
	new_first_name = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder': 'update first name'}))
	new_last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'update last name'}))
	new_email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'update email'}))
