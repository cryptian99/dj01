#
#
# Load games table
#
import sys, re

club_names = {}
club_ids = {}


def connect_to_db(name, provider='sqlite', file=None):
    if provider == 'sqlite':
        try:
            pass
        except Exception, ex:
            print 'Import exception for provider %s, reason "%s"' % (provider, repr(ex))
            return (False)
        import sqlite3

        try:
            conn = sqlite3.connect(file)
            cur = conn.cursor()
        except Exception, ex:
            print 'Unable to either connect or to open the db %s, reason "%s"' % (name, repr(ex))
            return (False)
        return (conn, cur)
    elif provider == 'mysql':
        print 'import %s not implemented yet' % provider
        return (False)
    elif provider == 'db2':
        print 'import %s not implemented yet' % provider
        return (False)
    elif provider == 'postgresql':
        print 'import %s not implemented yet' % provider
        return (False)
    else:
        print 'Provider %s not recognised/supported'
    return (False)


def select_all_clubs(connector, cursor, db='premier', table='club'):
    global club_names, club_ids
    my_table = '%s_%s' % (db, table)
    sql = "SELECT * FROM %s" % (my_table)
    try:
        cursor.execute(sql)
    except Exception, ex:
        print 'Unable to fetch records from table %s, reason "%s"' % (my_table, repr(ex))
        return (False)
    result = cursor.fetchall()
    for t in result:
        club_names[t[1]] = t[0]
        club_ids[t[0]] = t[1]
    #print club_names
    #print '-' * 80
    #print club_ids
    return (len(club_names))


def select_club_by_name(connector, cursor, name, db='premier', table='club'):
    my_table = '%s_%s' % (db, table)
    sql = "SELECT * FROM %s WHERE name_club = %s" % (my_table, str(name))
    #print sql
    try:
        cursor.execute(sql)
    except Exception, ex:
        print 'Unable to fetch record for club %s, reason "%s"' % (str(id), repr(ex))
        return (False)
    #result = cursor.fetchone()
    result = cursor.fetchall()
    #print result
    return (result)


def select_club_by_id(connector, cursor, id, db='premier', table='club'):
    my_table = '%s_%s' % (db, table)
    sql = "SELECT * FROM %s WHERE id_club = %s" % (my_table, str(id))
    try:
        cursor.execute(sql)
    except Exception, ex:
        print 'Unable to fetch record for club %s, reason "%s"' % (str(id), repr(ex))
        return (False)
    result = cursor.fetchone()
    return (result)


def quoted(str):
    if str and len(str) and str[0] in "\"'" and str[-1] in "\"'":
        return (True)
    return (False)


def unquote(str):
    #print 'unquote %s' % str
    while str.startswith("'") or str.startswith('"'):
        str = str[1:]
    while str.endswith("'") or str.endswith('"'):
        str = str[:-1]
    #print 'unquoted %s' % str
    return (str)


def game_exists(connector, cursor, values_dic, db='premier', table='game'):
    #print 'in: game_exists'
    my_table = '%s_%s' % (db, table)
    if not cursor:
        print 'DB table cursor for %s has not been set up' % my_table
        return (False)
    if not isinstance(values_dic, dict):
        print 'A dictionary of key/value pairs has not been provided or is of the wrong type'
        return (False)
    values_dic['table'] = my_table
    sql = 'SELECT COUNT(*) FROM %s WHERE home_id = %s AND away_id = %s' % \
          (my_table, values_dic['home_id'], values_dic['away_id'])
    #print sql
    query = cursor.execute(sql)
    fetch = query.fetchall()
    result = fetch[0][0]
    #print 'count result is %s' % result
    if result:
        sql = "DELETE FROM %s WHERE home_id = %s AND away_id = %s" % \
                (my_table, values_dic['home_id'], values_dic['away_id'])
        update = cursor.execute(sql)
        #print update
        connector.commit()
        result = create_game(connector, cursor, values_dic)
        #print 'create_game returns result %s' % result
        return(result)
    return(0)


def format_datetime(game_date, game_time):
    dt = "%s/%s/%s %s:%s:00" % (game_date[0:4], game_date[4:6], game_date[6:8], game_time[0:2], game_time[2:4])
    return (dt)

import copy

def create_game(connector, cursor, values_dic):
    #print 'create_game: %s' % values_dic
    my_table = values_dic['table']
    local_dic = copy.deepcopy(values_dic)
    del local_dic['table']
    del local_dic['home_club']
    del local_dic['away_club']
    local_dic['game_datetime'] = format_datetime(values_dic['game_date'], values_dic['game_time'])
    del local_dic['game_date']
    del local_dic['game_time']
    columns = ",".join(local_dic.keys())
    for k in local_dic.keys():
        if not isinstance(local_dic[k], int) and not local_dic[k].isdigit() and not quoted(local_dic[k]):
            local_dic[k] = '"%s"' % local_dic[k]
    values = ",".join([local_dic[key] for key in local_dic.keys()])
    sql = 'INSERT INTO %s (%s) VALUES (%s)' % (my_table, columns, values)
    #print sql
    try:
        cursor.execute(sql)
    except Exception, ex:
        if 'not unique' in repr(ex):
            print 'A record for %s already exists. Ignored.' % (values.split(',')[0])
            return (True)
        else:
            print 'Unable to insert record into %s. Reason "%s"' % (my_table, repr(ex))
            return (False)
    connector.commit()
    return(True)

def update_game():
    pass

def load_record(connector, cursor, values_dic, db='premier', table='game'):
    global club_names, club_ids
    my_table = '%s_%s' % (db, table)
    values_dic['table'] = my_table
    if not cursor:
        print 'DB table cursor for %s has not been set up' % my_table
        return (False)
    if not isinstance(values_dic, dict):
        print 'A dictionary of key/value pairs has not been provided or is of the wrong type'
        return (False)
    #print 'home club -> %s' % (values_dic['home_club'])
    #print 'away club -> %s' % (values_dic['away_club'])
    home_club_name = unquote(values_dic['home_club'])
    if home_club_name in club_names:
        values_dic['home_id'] = str(club_names[home_club_name])
    else:
        print 'Club %s not recognised in DB' % (home_club_name)
        return (False)
    away_club_name = unquote(values_dic['away_club'])
    if away_club_name in club_names:
        values_dic['away_id'] = str(club_names[away_club_name])
    else:
        print 'Club %s not recognised in DB' % (away_club_name)
        return (False)
    if game_exists(connector, cursor, values_dic):
        return (True)
    if create_game(connector, cursor, values_dic):
        return(True)
    # test value inserted

    # TODO

    return (False)


def load_records(connector, cursor, filename):
    global clubs
    print 'Loading game records'
    f = open(filename)
    match = f.readline()
    while match:
        match = re.sub('[\n\r]', '', match)
        values = match.split(',')
        #print match
        if len(match) < 11:
            print 'Skipped game record "%s"' % match
        else:
            values_dict = {'week_number': values[0],
                           'game_date': values[1],
                           'game_time': values[2],
                           'home_club': values[3],
                           'away_club': values[10]}
            result = load_record(connector, cursor, values_dict)
        match = f.readline()
    # end while
    f.close()


def main(db_name, game_file):
    db_connector, db_cursor = connect_to_db(db_name, file='db.sqlite3')
    if not db_cursor:
        sys.exit(1)
    club_count = select_all_clubs(db_connector, db_cursor)
    print 'Found %d clubs' % club_count
    if load_records(db_connector, db_cursor, game_file):
        sys.exit(0)
    sys.exit(9)


if __name__ == '__main__':
    main('db.sqlite3_1', sys.argv[1])

