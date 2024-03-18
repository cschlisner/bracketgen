from django.test import TestCase
from django.contrib.auth.models import User
from bracketgen.models import Tournament, Player, Round, Match
from bracketgen.forms import CreateTournamentForm
# Create your tests here.

class CreateTournamentFormTest(TestCase):

    def test_form_field_label(self):
        form = CreateTournamentForm()        
        self.assertTrue(form.fields['tournament_name'].label == None or form.fields['tournament_name'].label == 'tournament_name')

    def test_empty_string_entry(self):
        tourney_name = ''
        form_data = {'tournament_name': tourney_name}
        form = CreateTournamentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_1_char_string_entry(self):
        tourney_name = 'a'
        form_data = {'tournament_name': tourney_name}
        form = CreateTournamentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_26_char_string_entry(self):
        tourney_name = 'abcdefghijklmnopqrstuvwxyz'
        form_data = {'tournament_name': tourney_name}
        form = CreateTournamentForm(data=form_data)
        self.assertFalse(form.is_valid())    