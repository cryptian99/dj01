#!/usr/bin/python
# __author__ = 'peterhaydon'

import sqlite3
from schema import schema, contribution_default
#from premier.db.club import get_squad_numbers
from premier.db.goal import get_goals_by_contribution, goals_by_club_time

CONTRIB_ID=0
GAME_ID=1
ON_MIN=2
OFF_MIN=3
YELLOW=4
RED=5

def get_player_stats(club_id, squad_number):
    #print schema
    connector = sqlite3.connect(schema)
    cursor = connector.cursor()
    sql = "SELECT id_contribution, id_game, on_minutes, off_minutes, yellow_count, red_count " \
               " FROM %s WHERE id_club = %s AND squad_number = %s" % \
          (contribution_default, club_id, squad_number)
    try:
        query = cursor.execute(sql)
        result = query.fetchall()
    except Exception, ex:
        print 'Unable to query table %s for data. %s' % (contribution_default, repr(ex))
        return(None)

    yellows = reds = total_mins = starts = subs = subbed = goals_for = goals_against = 0
    appearances = len(result)
    print 'got %s results' % len(result)
    for x in result:
        print x
    print '*' * 60
    for contribution in result:
        yellows += contribution[YELLOW]
        reds += contribution[RED]
        if contribution[ON_MIN] == 1:
            # a starter
            starts += 1
            total_mins += contribution[OFF_MIN]
            if contribution[OFF_MIN] != 90:
                subbed += 1
        elif contribution[ON_MIN] != 0:
            # a substitute
            subs += 1
            if contribution[ON_MIN] > 90:
                total_mins += (95 - contribution[ON_MIN])
            if contribution[OFF_MIN] <= 90:
                total_mins += 1 + (contribution[OFF_MIN] - contribution[ON_MIN])
        fors, against = get_goals_by_contribution(connector, contribution[CONTRIB_ID])
        goals_for += fors
        goals_against += against
    cursor.close()
    connector.close()
    response = { 'appear':appearances, 'start':starts, 'sub':subs, 'subbed':subbed, 'minutes':total_mins,
               'for':goals_for, 'own':goals_against, 'yellow':yellows, 'red':reds, 'squad':squad_number,
               'games':result}
    print response
    return(response)

def get_player_stats_for_game(game_id, player_id):
    pass

def get_players_stats(club_id):
    players = []
    squad_list = get_squad_numbers(club_id, ordered=True)
    #print 'squad = %s' % squad_list
    team_stats = []
    for s in squad_list:
        result = get_player_stats(club_id, s)
        team_stats += [result]
    return(team_stats)

def get_goal_stats(club_id):
    connector = sqlite3.connect(schema)
    fest = goals_by_club_time(connector, club_id)
    return(fest)


if __name__ == '__main__':
    a = 1
    b = 17
    x = get_player_stats(a,b)
    print 'Club=%s, Squad=%s: %s' % (a, b, x)
    x = get_goal_stats(a)
    print ''
    all_stats = get_players_stats(3)
    for stat in all_stats:
        print stat






