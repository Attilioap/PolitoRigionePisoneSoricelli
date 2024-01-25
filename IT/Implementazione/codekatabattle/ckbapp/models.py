from django.db import models

class User(models.Model):
    fullName = models.CharField(max_length=255, default='')
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, default='')
    password = models.CharField(max_length=255)
    role = models.BooleanField()

class Student(User):
    pass

class Educator(User):
    pass

class Battle(models.Model):
    name = models.CharField(max_length=255)
    maxStudentsForTeam = models.IntegerField()
    registrationDeadline = models.DateField()
    submissionDeadline = models.DateField()
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, related_name='battles')
    teams = models.ManyToManyField('Team', related_name='battles_participated')
    educators = models.ManyToManyField('Educator', related_name='battles_managed')

class Team(models.Model):
    name = models.CharField(max_length=255)
    numTeammates = models.IntegerField()
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)
    members = models.ManyToManyField(Student, related_name='teams_joined')

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    registrationDeadline = models.DateField()
    endingDate = models.DateField()
    description = models.TextField()
    students = models.ManyToManyField(Student, related_name='tournaments_participated')
    educators = models.ManyToManyField(Educator, related_name='tournaments_managed')
