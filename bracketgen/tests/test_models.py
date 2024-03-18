from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

from bracketgen.models import Tournament, Player, Round, Match

class TournamentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        User.objects.create(username='nameuser', password='wordpass', first_name='First', last_name='Last')
        Tournament.objects.create(name='TournamentName', reference_code='Tour123', user_owner=User.objects.get(id=1))
        Player.objects.create(name='P1')
        Player.objects.create(name='P2')
    
    def test_tournament_owner(self):
        tourney = Tournament.objects.get(id=1)
        user = User.objects.get(id=1)
        field_label = tourney.user_owner
        self.assertEquals(field_label,user)
    
    def test_tournament_default_status(self):
        tourney = Tournament.objects.get(id=1)
        field_label = tourney.status
        self.assertEquals(field_label,'w')

    def test_tournament_default_current_round(self):
        tourney = Tournament.objects.get(id=1)
        field_label = tourney.current_round
        self.assertEquals(field_label,1)

    def test_name_max_length(self):
        tourney = Tournament.objects.get(id=1)
        field_label = tourney._meta.get_field('name').max_length
        self.assertEquals(field_label,20)

    def test_player_name(self):
        p =  Player.objects.get(id=1)
        field_label = p.name
        self.assertEquals(field_label,'P1')

    def test_player_name_2(self):
        p =  Player.objects.get(id=2)
        field_label = p.name
        self.assertEquals(field_label,'P2')

    def test_player_default_wins(self):
        p = Player.objects.get(id=1)
        field_label = p.wins
        self.assertEquals(field_label,0)

    def test_player_default_losses(self):
        p = Player.objects.get(id=1)
        field_label = p.losses
        self.assertEquals(field_label,0)

    def test_player_default_rank(self):
        p = Player.objects.get(id=1)
        field_label = p.rank
        self.assertEquals(field_label,0)

    def test_player_default_bye(self):
        p = Player.objects.get(id=1)
        field_label = p.bye
        self.assertFalse(field_label)
    
    