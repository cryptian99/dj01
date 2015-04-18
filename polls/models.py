import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')


	def __unicode__(self):
		return(self.question_text)

	def was_published_recently(self):
		return(self.pub_date >= (timezone.now() - datetime.timedelta(days=1)))

class Choice(models.Model):
	question = models.ForeignKey(Question)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __unicode__(self):
		return(self.choice_text)


class Clubs(models.Model):
	id_club = models.IntegerField(primary_key=True)
	name_club = models.CharField(max_length=63)

class Players(models.Model):
    id_player = models.IntegerField(primary_key=True)
    squad_number = models.IntegerField()
    club_id = models.IntegerField()
    aliases = models.CharField(max_length=255)
    given_name = models.CharField(max_length=63)
    surname = models.CharField(max_length=63)

class Games(models.Model):
    id_game = models.IntegerField(primary_key=True)
    week_number = models.IntegerField()
    game_datetime = models.DateTimeField()
    home_id = models.IntegerField()
    away_id = models.IntegerField()
    home_goals = models.IntegerField()
    away_goals = models.IntegerField()

class Contributions(models.Model):
    id_contribution = models.IntegerField(primary_key=True)
    id_game = models.IntegerField()
    id_club = models.IntegerField()
    squad_number = models.IntegerField()
    on_minutes = models.IntegerField()
    off_minutes = models.IntegerField()
    yellow_count = models.IntegerField()
    red_count = models.IntegerField()

class Goals(models.Model):
    id_goal = models.IntegerField(primary_key=True)
    id_contribution = models.IntegerField()
    at_minutes = models.IntegerField()
    id_goaltype = models.IntegerField()




