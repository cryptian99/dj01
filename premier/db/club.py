#!/usr/bin/python
# __author__ = 'peterhaydon'

import sqlite3
from schema import schema, db, make_table_name, club_default, game_default, player_default
from premier.db.contribution import get_player_stats

def get_clubs(by_name=True):
    if by_name:
        sql = "SELECT id_club, name_club FROM %s ORDER BY name_club" % club_default
    else:
        sql = "SELECT id_club, name_club FROM %s ORDER BY id_club" % club_default
    connector = sqlite3.connect(schema)
    cursor = connector.cursor()
    query = cursor.execute(sql)
    result = query.fetchall()
    cursor.close()
    connector.close()
    return(result)

def get_club_data(club_id, ordered=True):
    sql = "SELECT name_club FROM %s WHERE id_club = %s" % (club_default, club_id)
    connector = sqlite3.connect(schema)
    cursor = connector.cursor()
    query = cursor.execute(sql)
    result_1 = query.fetchall()
    if ordered:
        sql = "SELECT squad_number, given_name, surname FROM %s WHERE club_id = %s ORDER BY squad_number" % (player_default, club_id)
    else:
        sql = "SELECT squad_number, given_name, surname FROM %s WHERE club_id = %s" % (player_default, club_id)
    query = cursor.execute(sql)
    result_2 = cursor.fetchall()
    cursor.close()
    connector.close()
    return({'club':result_1, 'player':result_2})

def get_squad_numbers(club_id, ordered=True):
    if ordered:
        sql = "SELECT DISTINCT squad_number FROM %s WHERE club_id = %s ORDER BY squad_number" % (player_default, club_id)
    else:
        sql = "SELECT DISTINCT squad_number FROM %s WHERE club_id = %s" % (player_default, club_id)
    #print sql
    connector = sqlite3.connect(schema)
    cursor = connector.cursor()
    query = cursor.execute(sql)
    squad = query.fetchall()
    result = [str(member[0]) for member in squad]
    #print result
    return(result)

def get_result_data(club_id, all=False):
    sql = """
            SELECT G.week_number as 'WEEK',
                G.game_datetime AS 'DATE',
                C1.name_club AS 'HOME',
                C2.name_club AS 'AWAY',
                G.home_goals AS 'FOR',
                G.away_goals AS 'AGAINST',
                C1.id_club AS CLUB
                FROM %s AS G
                JOIN %s AS C1 ON G.home_id = C1.id_club
                JOIN %s AS C2 ON G.away_id = C2.id_club
                WHERE G.home_id = %s OR G.away_id = %s
                ORDER BY G.week_number
            """ % (game_default, club_default, club_default, club_id, club_id)
    #print sql
    connector = sqlite3.connect('db.sqlite3')
    cursor = connector.cursor()
    query = cursor.execute(sql)
    db_result = query.fetchall()
    club_name = ''
    result = []
    for dbr in db_result:
        dbl = list(dbr)
        if not (dbl[4] == None or dbl[5] == None):
            #print 'club_id %s, dbl[6] = %s' % (club_id, dbl[6])
            if dbl[6] == int(club_id):
                club_name = dbl[2]
                #print 'at home',
                if dbl[4] > dbl[5]:
                    dbl += [3, 'W']
                elif dbl[4] < dbl[5]:
                    dbl += [0, 'L']
                else:
                    dbl += [1, 'D']
            else:
                #print 'away',
                club_name = dbl[3]
                if dbl[4] > dbl[5]:
                    dbl += [0, 'L']
                elif dbl[4] < dbl[5]:
                    dbl += [3, 'W']
                else:
                    dbl += [1, 'D']
            #print 'dbl: %s' % dbl
        elif all:
            dbl[4] = dbl[5] = ''
            dbl += ['', '']
        else:
            continue
        result += [dbl]
    #print 'result: %s' % result
    return(club_name, {'result':result})

def get_player_data(club_id, squad_number):
    sql = """
        SELECT C1.name_club, P.id_player, P.squad_number, P.surname, P.given_name, P.active
            FROM %s AS P
            JOIN %s AS C1 ON C1.id_club = P.club_id
            WHERE P.club_id = %s AND squad_number = %s""" \
                % (player_default, club_default, club_id, squad_number)
    connector = sqlite3.connect('db.sqlite3')
    cursor = connector.cursor()
    query = cursor.execute(sql)
    first_result = query.fetchall()
    #print 'get_player_data: first_result'
    #print first_result
    stats = get_player_stats(club_id, squad_number)
    #print 'get_player_data: stats'
    #print stats
    # turn dict to pre-ordered list
    key_order = ['start','minutes','for','own','appear','sub','subbed','yellow','red']
    stat_list = []
    for a_key in key_order:
        stat_list += [str(stats[a_key])]
    #print 'stat_list:',
    #print stat_list
    play_list = list(first_result[0][1:]) + stat_list
    #print 'play_list', play_list
    return({'club':first_result[0][0], 'player':play_list, 'games':stats['games']})

def get_club_name(club_id):
    sql = "SELECT name_club FROM %s WHERE id_club = %s" % (club_default, club_id)
    connector = sqlite3.connect('db.sqlite3')
    cursor = connector.cursor()
    query = cursor.execute(sql)
    result = query.fetchall()
    return(result[0])



