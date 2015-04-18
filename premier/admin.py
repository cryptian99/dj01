from django.contrib import admin

# Register your models here.
from premier.models import Club
admin.site.register(Club)

from premier.models import Player
admin.site.register(Player)

from premier.models import Game
admin.site.register(Game)

from premier.models import Contribution
admin.site.register(Contribution)

from premier.models import Goal
admin.site.register(Goal)
