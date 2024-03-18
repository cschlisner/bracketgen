from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

class Player(models.Model):
	"""
	Model representing a player (or team) -- 
	Contains details about the player including win/loss count
	"""

	name = models.CharField(max_length=20, help_text="Enter a player name")

	wins = models.SmallIntegerField(default=0)

	losses = models.SmallIntegerField(default=0)

	match = models.SmallIntegerField(default=0)

	# Rank in tournament (W/L ratio) or score
	rank = models.SmallIntegerField(default=0)

	bye = models.BooleanField(default=False)

	def set_bye(self, v):
		bye = v
		self.save()

	def __str__(self):
		return self.name

# single game between 2 players
class Match(models.Model):

	name = models.CharField(max_length=60, default="")

	index = models.SmallIntegerField(default=0)

	players = models.ManyToManyField(
		Player, 
		related_name="matches"
	)

	winner = models.ForeignKey(
		Player,
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		related_name="matches_won",
	)

	def declare_winner(self, p_name):
		w = self.players.get(name=p_name)
		print("Declaring Winner of %s: %s" % (self, w))
		self.winner = w
		self.save()
		self.round.all()[0].match_complete(self)

	def __str__(self):
		return self.name
	class Meta:
		ordering = [F('winner').asc(nulls_last=False)]

# list of matches 
class Round(models.Model):

	name = models.CharField(max_length=80, default="")

	index = models.SmallIntegerField()
	
	matches = models.ManyToManyField(
		Match, 
		related_name="round",
	)
	
	winners = models.ManyToManyField(Player)

	def new_match(self, p1, p2):
		m = Match(index=self.matches.count() + 1, name=("%s v. %s" % (p1, p2)))
		print("Creating match: %s" % m)
		m.save()
		m.players.add(p1)
		m.players.add(p2)
		self.matches.add(m)

	def match_complete(self, match):
		self.winners.add(match.winner)
		self.save()
		self.matches.remove()
		n_incomplete_matches = self.matches.filter(winner__isnull=True).count()
		print("Matches left in round %d: %d" % (self.index, n_incomplete_matches))
		if n_incomplete_matches == 0:
			self.tournament.all()[0].new_round()

	def __str__(self):
		return "%s-%d" % (self.name, self.index)

class Tournament(models.Model):
	"""
	Model representing a tournament -- 
	Contains data about status, administration, players, etc.
	"""

	name = models.CharField(max_length=20, help_text="Enter a tournament name")
	
	players = models.ManyToManyField(
		Player, 
		related_name="tounaments",
	)

	# Should be substr(tournamnet name) + substr(hash(tournament name + tournament ID))
	reference_code = models.CharField(max_length=10, null=True)
	
	current_round = models.SmallIntegerField(default=1)
	
	winner = models.ForeignKey(
		Player,
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		related_name="tournaments_won",
	)
	
	user_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	
	password = models.CharField(blank=True, null=True,max_length=50, help_text="Enter a tournament password")

	TOURNAMENT_STATUS = (
		('w', 'Waiting for players'),
		('a', 'Active'),
		('c', 'Completed')
	)

	status = models.CharField(max_length=1, choices=TOURNAMENT_STATUS, blank=True, default='w', help_text='Tournament status')

	user_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return self.name

	rounds = models.ManyToManyField(
		Round, 
		related_name="tournament", 
		blank=True,
	)

	def new_round(self):
		
		# add all players on initial round, else add all winners from previous match
		plist = list(self.players.all() if self.current_round == 1 else self.rounds.get(index=self.current_round-1).winners.all())
		
		n_byes = 0

		# figure out amount of players that will be competing in the 2nd round
		if self.current_round == 1:
			# find amount of players who will be in 2nd round (bye)
			powers_of_two = [2**i for i in range(10)]
			for i, pw in enumerate(powers_of_two):
				if pw > len(plist):
					n_byes = pw - len(plist) if len(plist) != powers_of_two[i-1] else 0
					break
			print("Players on bye (%d): "%n_byes,end='')
			for i in range(n_byes):
				plist[-1].bye = True
				plist[-1].save()
				print(plist[-1],end=', ')
				plist.remove(plist[-1])
			print()

		# add all players on bye
		elif self.current_round == 2:
			print("Adding players on bye: ",end='')
			# add all the players on bye / reset their status
			for player in self.players.filter(bye=True).all():
				print(player,end=', ')
				player.bye = False
				player.save()
				plist.append(player)
			print()

		# we have a tournament winner
		if len(plist) == 1:
			self.winner = plist[0]
			self.status = 'c'
		
		# create matches 
		else:
			newRound = Round(name=self.name)
			newRound.index = self.current_round
			newRound.save()
			print("Creating round: %d" % (newRound.index))
			print("plist: ", plist)

			# n_matches = int(len(plist) / 2)

			# print("nmatches: ", n_matches)

			# create all of the matches with sequential players
			while (len(plist) > 0):
				plr1 = plist.pop()
				plr2 = plist.pop()
				newRound.new_match(plr1, plr2)

			newRound.save()
			self.current_round += 1
			self.rounds.add(newRound)

		self.save()

	def __str__(self):
		return str(self.name)


