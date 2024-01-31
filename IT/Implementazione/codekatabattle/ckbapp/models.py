# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    # Additional fields specific to students

class Educator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    # Additional fields specific to educators


class TournamentLeaderboard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, related_name='tournament_leaderboard')
    # Add any additional fields specific to tournament leaderboard

class BattleLeaderboard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    battle = models.ForeignKey('Battle', on_delete=models.CASCADE, related_name='battle_leaderboard')
    # Add any additional fields specific to battle leaderboard

class TeamLeaderboard(models.Model):
    
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='leaderboard')
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    battle = models.ForeignKey('Battle', on_delete=models.CASCADE, related_name='team_leaderboard')
    # Add any additional fields specific to team leaderboard

class Battle(models.Model):
    name = models.CharField(max_length=255)
    maxStudentsForTeam = models.IntegerField()
    registrationDeadline = models.DateField()
    submissionDeadline = models.DateField()
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, related_name='battles')
    teams = models.ManyToManyField('Team', related_name='battles_participated')
    creator = models.ForeignKey(Educator, on_delete=models.CASCADE, related_name='battle_created', default=None)
    codeKata = models.FileField(upload_to='code_katas/', blank=False, null=False)

class Team(models.Model):
    name = models.CharField(max_length=255)
    numTeammates = models.IntegerField()
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name='teams_participated')
    members = models.ManyToManyField(Student, related_name='teams_joined')

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    registrationDeadline = models.DateField()
    endingDate = models.DateField()
    description = models.TextField()

    creator = models.ForeignKey(Educator, on_delete=models.CASCADE, related_name='tournaments_created', default=None)
    educators = models.ManyToManyField(Educator, related_name='tournaments_managed', blank=True)

    students = models.ManyToManyField(Student, related_name='tournaments_participated', blank=True)

class Invite(models.Model):
    inviting_student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invitations_sent')
    invited_student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invitations_received')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invitations_team', default=None)
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name='invitations')
    is_accepted = models.BooleanField(default=False)    
