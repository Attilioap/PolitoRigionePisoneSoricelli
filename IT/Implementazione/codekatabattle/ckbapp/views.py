from django.shortcuts import render
from .models import Tournament
from datetime import datetime

def tournament_list():
    tournaments = Tournament.objects.all()
    past_tournaments=[tournament for tournament in tournaments if tournament.endingDate < datetime.now().date()]
    ongoing_tournaments=[tournament for tournament in tournaments if tournament.endingDate >= datetime.now().date()]
    return ongoing_tournaments, past_tournaments

def educator_dash(request):
    ongoing_tournaments, past_tournaments=tournament_list()
    return render(request, 'ckbapp/educator_dashboard.html', {'ongoing_tournaments': ongoing_tournaments, 'past_tournaments' : past_tournaments})