import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Club(models.Model):
    id_club = models.AutoField(primary_key=True)
    name_club = models.CharField(max_length=63, unique=True)

class Player(models.Model):
    id_player = models.AutoField(primary_key=True)
    squad_number = models.IntegerField()
    club_id = models.ForeignKey(Club, verbose_name='id_club')
    surname = models.CharField(max_length=63, default=None)
    given_name = models.CharField(max_length=63, default=None)
    aliases = models.CharField(max_length=255, default=None)

class Game(models.Model):
    id_game = models.IntegerField(primary_key=True)
    week_number = models.IntegerField()
    game_datetime = models.DateTimeField()
    home_id = models.IntegerField()
    away_id = models.IntegerField()
    home_goals = models.IntegerField()
    away_goals = models.IntegerField()

class Contribution(models.Model):
    id_contribution = models.IntegerField(primary_key=True)
    id_game = models.IntegerField()
    id_club = models.IntegerField()
    squad_number = models.IntegerField()
    on_minutes = models.IntegerField()
    off_minutes = models.IntegerField()
    yellow_count = models.IntegerField()
    red_count = models.IntegerField()

class Goal(models.Model):
    id_goal = models.IntegerField(primary_key=True)
    id_contribution = models.IntegerField()
    at_minutes = models.IntegerField()
    id_goaltype = models.IntegerField()

class GoalType(models.Model):
    id_goaltype = models.IntegerField(primary_key=True)
    desc_goaltype = models.CharField(max_length=63)
    marker_goaltype = models.CharField(max_length=1)
    increment_goaltype = models.IntegerField()

