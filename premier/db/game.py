#!/usr/bin/python
# __author__ = 'peterhaydon'

import sqlite3
from datetime import datetime
from schema import schema, db, game_default, club_default, contribution_default

def get_club_fixtures(club_id):
    sql = """
        SELECT G.week_number, G.game_datetime, G.home_id, C1.name_club, G.away_id, C2.name_club, G.home_goals, G.away_goals
        FROM %s AS G
        JOIN %s AS C1 ON G.home_id = C1.id_club
        JOIN %s AS C2 ON G.away_id = C2.id_club
        WHERE G.home_id = %s OR G.away_id = %s
        ORDER BY G.week_number ASC
        """ % (game_default, club_default, club_default, club_id, club_id)
    connector = sqlite3.connect(schema)
    cursor = connector.cursor()
    query = cursor.execute(sql)
    result = query.fetchall()
    cursor.close()
    connector.close()
    output = []
    for record in result:
        #print 'RECORD:',record
        fixture = [record[0]]
        fixture += [record[1][8:10]+'-'+record[1][5:7]+'-'+record[1][0:4]]
        fixture += [record[1][11:16]]
        for item in record[2:]:
            if item or item == 0:
                fixture += [item]
            else:
                fixture += ['']
        output += [fixture]
    #print output
    return(output)

def get_game_by_id(game_id):
    if (game_id == 0 or game_id == None):
        print 'empty game_id'
        return(None)
    print 'game_id: %s' % game_id
    sql = """
        SELECT G.id_game, G.week_number, G.game_datetime, G.home_id, C1.name_club, G.away_id, C2.name_club, G.home_goals, G.away_goals
        FROM %s AS G
        JOIN %s AS C1 ON G.home_id = C1.id_club
        JOIN %s AS C2 ON G.away_id = C2.id_club
        WHERE G.id_game = %s
        ORDER BY G.week_number ASC
        """ % (game_default, club_default, club_default, game_id)
    connector = sqlite3.connect(schema)
    cursor = connector.cursor()
    query = cursor.execute(sql)
    result = query.fetchall()
    cursor.close()
    connector.close()
    print 'get_game:', result
    if result == []:
        return(None)
    return(result)

def _get_week_fixtures(week_id):
    pass

def get_game_by_team_week(home_club_id, away_club_id, week_id):
    pass

def set_game(home_club_id, away_club_id, week_number, details):

    pass
