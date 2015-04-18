#!/usr/bin/python
# __author__ = 'peterhaydon'

from schema import player_default

def get_player_by_club_squad(club_id, squad_number):
    sql = """
        SELECT id_player,