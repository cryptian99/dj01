#
#
#	Load match results into contribution & goals tables
#
import os, sys, re, datetime

from premier.db.schema import game_default, club_default, goaltype_default, player_default, goal_default, contribution_default

club_names = {}
club_ids = {}
goal_types = {}
goal_markers = {}
game_ids = []

def connect_to_db(name, provider='sqlite', file=None):
    if provider == 'sqlite':
        try:
            pass
        except Exception, ex:
            print 'Import exception for provider %s, reason "%s"' % (provider, repr(ex))
            return(False)
        import sqlite3
        try:
            conn = sqlite3.connect(file)
            cur = conn.cursor()
        except Exception, ex:
            print 'Unable to either connect or to open the db %s, reason "%s"' % (name, repr(ex))
            return(False)
        return(conn, cur)
    elif provider == 'mysql':
        print 'import %s not implemented yet' % provider
        return(False)
    elif provider == 'db2':
        print 'import %s not implemented yet' % provider
        return(False)
    elif provider == 'postgresql':
        print 'import %s not implemented yet' % provider
        return(False)
    else:
        print 'Provider %s not recognised/supported'
        return(False)
    return(False)

def select_all_goaltypes(connector, cursor, db='premier', table='goaltype'):
    global goal_types, goal_markers
    my_table = goaltype_default
    sql = "SELECT id_goaltype,desc_goaltype,marker_goaltype,increment_goaltype FROM %s" % (my_table)
    try:
        cursor.execute(sql)
    except Exception, ex:
        print 'Unable to fetch records from table %s, reason "%s"' % (my_table, repr(ex))
        return(False)
    result = cursor.fetchall()
    #print result
    for t in result:
        #print t
        if t[2] == '':
            t = (t[0], t[1], '-', t[3])
        goal_types[t[0]] = (t[1], t[2], t[3])
        goal_markers[t[2]] = (t[0], t[3])
    #print goal_markers
    return(len(goal_types.keys()))

def select_all_clubs(connector, cursor, db='premier', table='club'):
    global club_names, club_ids
    my_table = club_default
    sql = "SELECT * FROM %s" % (my_table)
    try:
        cursor.execute(sql)
    except Exception, ex:
        print 'Unable to fetch records from table %s, reason "%s"' % (my_table, repr(ex))
        return(False)
    result = cursor.fetchall()
    for t in result:
        club_names[t[1]] = t[0]
        club_ids[t[0]] = t[1]
    #print club_names
    #print '-' * 80
    #print club_ids
    return(len(club_names))

def select_club_by_name(connector, cursor, name, db='premier', table='club'):
    my_table = club_default
    sql = "SELECT * FROM %s WHERE name_club = %s" % (my_table, str(name))
    #print sql
    try:
        cursor.execute(sql)
    except Exception, ex:
        print 'Unable to fetch record for club %s, reason "%s"' % (str(id), repr(ex))
        return(False)
    #result = cursor.fetchone()
    result = cursor.fetchall()
    #print result
    return(result)

def select_club_by_id(connector, cursor, id, db='premier', table='club'):
    my_table = club_default
    sql = "SELECT * FROM %s WHERE id_club = %s" % (my_table, str(id))
    try:
        cursor.execute(sql)
    except Exception, ex:
        print 'Unable to fetch record for club %s, reason "%s"' % (str(id), repr(ex))
        return(False)
    result = cursor.fetchone()
    return(result)

def quoted(str):
    if str and len(str) and str[0] in "\"'" and str[-1] in "\"'":
        return(True)
    return(False)

def unquote(str):
    #print 'unquote %s' % str
    while str.startswith("'") or str.startswith('"'):
        str = str[1:]
    while str.endswith("'") or str.endswith('"'):
        str = str[:-1]
    #print 'unquoted %s' % str
    return(str)

def game_exists(connector, cursor, values_dic, db='premier', table='game'):
    my_table = game_default
    if not cursor:
        print 'DB table cursor for %s has not been set up' % my_table
        return(False)
    if not isinstance(values_dic, dict):
        print 'A dictionary of key/value pairs has not been provided or is of the wrong type'
        return(False)
    sql = 'SELECT COUNT(*) FROM %s WHERE home_id = %s AND away_id = %s' % \
        (my_table, values_dic['home_id'], values_dic['away_id'])
    #print sql
    query = cursor.execute(sql)
    fetch = query.fetchall()
    result = fetch[0][0]
    if result:
        sql = "SELECT id_game FROM %s WHERE home_id = %s AND away_id = %s" % \
        (my_table, values_dic['home_id'], values_dic['away_id'])
        #print sql
        cursor.execute(sql)
        query = cursor.fetchall()
        result = query[0][0]
    #print result
    return(result)

def player_exists(connector, cursor, club_id, squad_number, db='premier', table='player'):
    my_table = player_default
    if not squad_number:
        return(0)
    sql = "SELECT id_player FROM %s WHERE squad_number = %s AND club_id = %s" % (my_table, squad_number, club_id)
    query = cursor.execute(sql)
    fetch = query.fetchall()
    if fetch:
        return(fetch[0][0])
    return(0)

def get_contribution(connector, cursor, game_no, club_no, squad_number, db='premier', table='contribution'):
    my_table = contribution_default
    sql = "SELECT COUNT(*) FROM %s WHERE id_game = %s AND id_club = %s AND squad_number = %s" % \
        (my_table, game_no, club_no, squad_number)
    #print sql
    cursor.execute(sql)
    query = cursor.fetchall()
    result = query[0][0]
    #print 'First result is %s' % result
    if result:
        sql = "SELECT id_contribution FROM %s WHERE id_game = %s AND id_club = %s AND squad_number = %s" %\
            (my_table, game_no, club_no, squad_number)
        #print sql
        cursor.execute(sql)
        query = cursor.fetchall()
        result = query[0][0]
        #print 'Second result is %s' % result
    return(result)

def make_contribution(connector, cursor, game_no, club_no, play_data, db='premier', table='contribution'):
    my_table = contribution_default
    columns = "id_game,id_club,squad_number,on_minutes,off_minutes,yellow_count,red_count"
    values = "%s,%s,%s,%s,%s,%s,%s" % (str(game_no),str(club_no),\
                    play_data[1],play_data[2],play_data[3],\
                    play_data[5],play_data[6])
    #print 'make_contribution: %s' % values
    contribution_id = get_contribution(connector, cursor, game_no, club_no, play_data[1])
    #print 'contribution_id = %s' % contribution_id
    if not contribution_id:
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (my_table, columns, values)
    else:
        sql = """UPDATE %s SET on_minutes = %s, off_minutes = %s, yellow_count = %s, red_count = %s
            WHERE id_contribution = %s""" % \
            (my_table, play_data[2], play_data[3], play_data[5], play_data[6], contribution_id)
    #print sql
    try:
        cursor.execute(sql)
    except Exception, ex:
        print 'Unable to execute: %s (%s)' % (sql, repr(ex))
        return(0)
    connector.commit()
    sql = "SELECT id_contribution FROM %s WHERE id_game = %s AND id_club = %s AND squad_number = %s" % \
        (my_table, game_no, club_no, play_data[1])
    cursor.execute(sql)
    query = cursor.fetchall()
    contribution_id = query[0][0]
    return(contribution_id)

def update_goals(connector, cursor, game_id, goals, contribution_id, this_team_id, that_team_id, db='premier'):
    global goal_markers
    my_table = goal_default
    if not goals or goals == '':
        return
    goals = unquote(goals)
    #print goals,
    goal_info = goals.split('+')
    #print goal_info
    for goal in goal_info:
        if 'o' in goal:
            goal_type = goal_markers['o'][0]
            goal_added = goal_markers['o'][1]
        elif 'p' in goal:
            goal_type = goal_markers['p'][0]
            goal_added = goal_markers['p'][1]
        elif goal.isdigit():
            if int(goal) and goal:
                goal_type = goal_markers["-"][0]
                goal_added = goal_markers["-"][1]
            else:
                continue
        else:
            print 'Unrecognised goal qualifier string "%s" found. Ignored' % str(goal)
            continue
        goal_time = re.sub('[a-z]','',goal)
        sql = "SELECT COUNT(*) FROM %s WHERE id_contribution = %s AND at_minutes = %s AND id_goaltype = %s" %\
            (my_table, contribution_id, goal_time, goal_type)
        #print sql
        cursor.execute(sql)
        query = cursor.fetchall()
        result = query[0][0]
        if not result:
            sql = "INSERT INTO %s (id_contribution,at_minutes,id_goaltype) VALUES (%s,%s,%s)" %\
                (my_table, contribution_id, goal_time, goal_type)
            cursor.execute(sql)
            connector.commit()

def get_contributions(connector, cursor, game_id, club_id, db='premier', table='contribution'):
    my_table = contribution_default
    sql = "SELECT id_contribution FROM %s WHERE id_game = %s AND id_club = %s" % \
            (my_table, game_id, club_id)
    cursor.execute(sql)
    query = cursor.fetchall()
    contributions = []
    for result in query:
        #print result
        #print result[0]
        contributions = contributions + [result[0]]
    #print 'contributions = %s' % contributions
    return(contributions)

def get_goal_totals(connector, cursor, contributions, db='premier', table='goal'):
    my_table = goal_default
    contribution = ','.join('%s' % contributor for contributor in contributions)
    sql = 'SELECT id_goaltype FROM %s WHERE id_contribution IN (%s)' % \
        (my_table, contribution)
    #print sql
    cursor.execute(sql)
    query = cursor.fetchall()
    #for q in query:
    #	print q
    count_for = count_against = 0
    for result in query:
        #print 'goaltype found = %d' % result[0]
        if result[0] in [0, 1]:
            count_for += 1
        if result[0] == 2:
            #print 'AGAINST'
            count_against += 1
    #print 'for: %s, against: %s' % (count_for, count_against)
    return(count_for, count_against)

def apply_game_result(connector, cursor, game_id, home, away, db='premier', table='game'):
    my_table = game_default
    sql = 'UPDATE %s SET home_goals = %s, away_goals = %s WHERE id_game = %s' % \
        (my_table, home, away, game_id)
    print 'update result: %s' % sql
    cursor.execute(sql)
    connector.commit()

def update_games(connector, cursor, game_ids, db='premier', table='game'):
    my_table = game_default
    for game_id in game_ids:
        sql = "SELECT home_id,away_id FROM %s WHERE id_game = %s" % (my_table, game_id)
        cursor.execute(sql)
        query = cursor.fetchall()
        home_id, away_id = query[0][0:2]
        #print 'game %s, home %s, away %s' % (game_id, home_id, away_id)
        home_contributions = get_contributions(connector, cursor, game_id, home_id)
        away_contributions = get_contributions(connector, cursor, game_id, away_id)
        home_for, home_against = get_goal_totals(connector, cursor, home_contributions)
        away_for, away_against = get_goal_totals(connector, cursor, away_contributions)
        home_goals = home_for + away_against
        away_goals = away_for + home_against
        #print 'result is %s - %s' % (home_goals, away_goals)
        apply_game_result(connector, cursor, game_id, home_goals, away_goals)

def format_datetime(game_date, game_time):
    dt = "%s/%s/%s %s:%s:00" % (game_date[0:4],game_date[4:6],game_date[6:8],game_time[0:2],game_time[2:4])
    return(dt)


def create_game(connector, cursor, values_dic):
    pass

def update_game_time(connector, cursor, game_id, values_dic):
    my_table = game_default
    #print values_dic
    dt = format_datetime(values_dic['game_date'], values_dic['game_time'])
    #print dt
    sql = "UPDATE %s SET game_datetime='%s' WHERE id_game = %s" % \
          (my_table, dt, game_id)
    #print sql
    cursor.execute(sql)
    connector.commit()

def load_record(connector, cursor, values_dic, db='premier', table='contribution'):
    global club_names, club_ids, game_ids
    my_table = contribution_default
    if not cursor:
        print 'DB table cursor for %s has not been set up' % my_table
        return(False)
    if not isinstance(values_dic, dict):
        print 'A dictionary of key/value pairs has not been provided or is of the wrong type'
        return(False)
    #print 'home club -> %s' % (values_dic['home_stats'][0])
    #print 'away club -> %s' % (values_dic['away_stats'][0])
    # home_stats is a tuple comprising columns 4-10 of the CSV file
    # away_stats is a tuple comprising columns 11-17 of the CSV file
    # tuple lists:
    #   [0] club name
    #   [1] squad-number
    #   [2] start-minutes
    #   [3] end-minutes
    #   [4] goals-info
    #   [5] yellows
    #   [6] reds
    # Verify home club name/get db id
    home_club_name = unquote(values_dic['home_stats'][0])
    if home_club_name in club_names:
        values_dic['home_id'] = str(club_names[home_club_name])
    else:
        print 'Club %s not recognised in DB' % (home_club_name)
        return(False)
    # Verify away club name/get db id
    away_club_name = unquote(values_dic['away_stats'][0])
    if away_club_name in club_names:
        values_dic['away_id'] = str(club_names[away_club_name])
    else:
        print 'Club %s not recognised in DB' % (away_club_name)
        return(False)
    if not player_exists(connector, cursor, values_dic['home_id'], values_dic['home_stats'][1]):
        print 'Unable to identify player #%s for home team %s. Ignored' % \
                (values_dic['home_stats'][1], home_club_name)
        return(False)
    #print 'Found player #%s for %s' % (values_dic['home_stats'][1], home_club_name)
    if not player_exists(connector, cursor, values_dic['away_id'], values_dic['away_stats'][1]):
        print 'Unable to identify player #%s for away team %s. Ignored' % \
                (values_dic['away_stats'][1], away_club_name)
        return(False)
    #print 'Found player #%s for %s' % (values_dic['away_stats'][1], away_club_name)

    game_id = 0
    while game_id < 1:
        game_id = game_exists(connector, cursor, values_dic)
        if not game_id:
            game_id = create_game(connector, cursor, values_dic)
        else:
            update_game_time(connector, cursor, game_id, values_dic)

    # end while
    if not game_id:
        print 'Unable to find/create game for %s vs %s' % (home_club_name, away_club_name)
        return(False)
    #print 'game_id = %d' % game_id
    if game_id not in game_ids:
        game_ids.append(game_id)
        #print 'games: ' + ','.join("%s" % game for game in game_ids)
    home_contrib = make_contribution(connector, cursor, game_id, values_dic['home_id'], values_dic['home_stats'])
    if not home_contrib:
        print 'Unable to create contribution record for player #%s at %s' % \
            (values_dic['home_stats'][1], home_club_name)
        return(False)
    away_contrib = make_contribution(connector, cursor, game_id, values_dic['away_id'], values_dic['away_stats'])
    if not away_contrib:
        print 'Unable to create contribution record for player #%s at %s' % \
            (values_dic['away_stats'][1], away_club_name)
        return(False)

    # Update goals table
    home_goals = values_dic['home_stats'][4]
    if home_goals and not (home_goals == '' or home_goals == '0'):
        update_goals(connector, cursor, game_id, home_goals, home_contrib, values_dic['home_id'], values_dic['away_id'])
    away_goals = values_dic['away_stats'][4]
    if away_goals and not (away_goals == '' or away_goals == '0'):
        update_goals(connector, cursor, game_id, away_goals, away_contrib, values_dic['away_id'], values_dic['home_id'])

    return(True)

def load_records(connector, cursor, filename):
    global clubs, game_ids
    print 'Loading game result records'
    f = open(filename)
    match = f.readline()
    while match:
        match = re.sub('[\n\r]','',match)
        values = match.split(',')
        #print match
        if len(values) < 17 or values[4] == '':
            print 'Skipped game record "%s"' % match
        else:
            values_dict = { 'week_number':values[0],
                    'game_date':values[1],
                    'game_time':values[2],
                    'home_stats':(values[3:10]),
                    'away_stats':(values[10:])}
            result = load_record(connector, cursor, values_dict)
        match = f.readline()
    # end while
    f.close()
    update_games(connector, cursor, game_ids)

def main(db_name, game_file):
    if not os.access(game_file, os.R_OK):
        print 'Cannot find the results file %s' % game_file
        sys.exit(2)
    db_connector, db_cursor = connect_to_db(db_name, file='db.sqlite3')
    if not db_cursor:
        sys.exit(1)
    types_count = select_all_goaltypes(db_connector, db_cursor)
    #print 'Found %d goal types' % types_count
    club_count = select_all_clubs(db_connector, db_cursor)
    #print 'Found %d clubs' % club_count
    if load_records(db_connector, db_cursor, game_file):
        sys.exit(0)
    sys.exit(9)

if __name__ == '__main__':
    main('db.sqlite3', sys.argv[1])

