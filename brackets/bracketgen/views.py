from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse, reverse_lazy
from .models import Tournament, Player, Match
from .forms import CreateTournamentForm, JoinTournamentForm, GoToTournamentForm, UpdateUserInfo, AuthTournamentForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

import random 
import hashlib
def hex_digest(s):
	stng = str(s)
	m = hashlib.md5()
	m.update(stng.encode('utf-8'))
	return m.hexdigest()


def index(request):
	joinform = GoToTournamentForm()
	createform = CreateTournamentForm()

	if request.method == 'POST':
		if (request.POST['form'] == "join"):
			form = GoToTournamentForm(request.POST)
			if form.is_valid():
				return HttpResponseRedirect(reverse('tournament', args=[form.cleaned_data['reference_code']]))
			#else: return HttpResponseNotFound("no matching tournament")
		
		elif (request.POST['form'] == "create"):
			form = CreateTournamentForm(request.POST)
			if form.is_valid():
				newTournament = Tournament()
				newTournament.name = form.cleaned_data['tournament_name']
				newTournament.password = form.cleaned_data['tournament_password']
				newTournament.save()

				newTournament.reference_code = newTournament.name[:4].replace(" ","")
				newTournament.reference_code += hex_digest(str(newTournament.id)+newTournament.name)[:3]

				newTournament.save()

				if request.user.is_authenticated:
					newTournament.user_owner = request.user
					newTournament.save()
				else:
					if request.session.get('tournaments_created') is None:
						request.session['tournaments_created'] = []

					request.session['tournaments_created'].append(newTournament.reference_code)
					request.session.save()
				
				return HttpResponseRedirect(reverse('tournament', args=[newTournament.reference_code]))

	return render(request, 'index.html', {'joinform': joinform, 'createform': createform})

def tournament(request, id):
	# get tournament by id 
	# print("sess_: %s"%request.session)
	# print("sess_tauthed: %s"%request.session.get('tournaments_authed'))
	# print("sess_tjoined: %s"%request.session.get('tournaments_joined'))
	# print("sess_tcreated: %s"%request.session.get('tournaments_created'))

	tournament = get_object_or_404(Tournament, reference_code=id)
	isOwner = tournament.user_owner == request.user or id in request.session.get('tournaments_created',[])

	if request.method == 'POST':
		if (request.POST['form'] == "authJoin"):
			print("AuthJoin")
			form = AuthTournamentForm(request.POST)
			if form.is_valid():
				if request.session.get('tournaments_authed') is None:
						request.session['tournaments_authed'] = {}
				request.session['tournaments_authed'][id] = form.cleaned_data['password']
				request.session.save()

		if (request.POST['form'] == "signup"):
			form = JoinTournamentForm(request.POST)
			if form.is_valid():
				if tournament.players.filter(name=form.cleaned_data['player_name']).count() > 0:
					return HttpResponseNotFound("player already in tournament")
				newPlayer = Player()
				newPlayer.name = form.cleaned_data['player_name']
				newPlayer.save()
				tournament.players.add(newPlayer)
				tournament.save()

				# allow the owner to manually add players
				if not isOwner: 
					if request.session.get('tournaments_joined') is None:
						request.session['tournaments_joined'] = {}
					request.session['tournaments_joined'][id] = newPlayer.name
					request.session.save()


		if (request.POST['form'] == "start"):
			tournament.status = 'a'
			tournament.new_round()
			return HttpResponseRedirect(reverse('tournament', args=[tournament.reference_code]))

		if (request.POST['form'] == "declare"):
			m = Match.objects.get(id=request.POST['match'])
			m.declare_winner(request.POST['winner'])


	ctx = {'tournament':tournament,'owner':isOwner}
	pname = None if isOwner else request.session.get('tournaments_joined',{id:None}).get(id)
	if pname is not None:
		ctx['joined_as'] = pname
	
	if tournament.status == 'w':
		
		if len(tournament.password) > 0 and request.session.get('tournaments_authed',{}).get(id) != tournament.password:
			ctx['authform'] = AuthTournamentForm()
		elif isOwner or pname is None: 
			ctx['playerform'] = JoinTournamentForm()

	# print("ctx: %s"%ctx.items())

	return render(request, 'tournament.html', context=ctx)

class myTournaments(LoginRequiredMixin,generic.ListView):
	"""
	Generic class-based view listing tournaments created by current user. 
	"""
	model = Tournament
	template_name ='my_tournaments.html'
	

	def get_queryset(self):
		return Tournament.objects.filter(user_owner=self.request.user)

class userInfo(LoginRequiredMixin,generic.ListView):
	"""
	Generic class-based view listing tournaments created by current user. 
	"""
	model = User
	template_name = 'user_info.html'
	paginate_by = 10

	def get_queryset(self):
		return User.objects.filter(username=self.request.user)
	
def updateUserInfo(request):
	if request.method == 'POST':
		
		form = UpdateUserInfo(request.POST)
		user_info = User.objects.get(username=request.user)

		if form.is_valid():
			if form.cleaned_data['new_first_name'] != '':
				user_info.first_name = form.cleaned_data['new_first_name']
			if form.cleaned_data['new_last_name'] != '':
				user_info.last_name = form.cleaned_data['new_last_name']
			if form.cleaned_data['new_email'] != '':
				user_info.email = form.cleaned_data['new_email']
			user_info.save()

	else:
		form = UpdateUserInfo()
	
	return render(request, 'userupdateform.html', {'form': form,})

class SignUp(generic.CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'