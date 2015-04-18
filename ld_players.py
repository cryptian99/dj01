#
#
# Load players table
#
import os, sys, re

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


def player_exists(connector, cursor, values_dic, db='premier', table='player'):
    my_table = '%s_%s' % (db, table)
    if not cursor:
        print 'DB table cursor for %s has not been set up' % my_table
        return (False)
    if not isinstance(values_dic, dict):
        print 'A dictionary of key/value pairs has not been provided or is of the wrong type'
        return (False)
    sql = 'SELECT id_player FROM %s WHERE club_id = %s AND squad_number = %s AND surname = "%s"' % \
          (my_table, values_dic['club_id'], values_dic['squad_number'], unquote(values_dic['surname']))
    #print sql
    query = cursor.execute(sql)
    fetch = query.fetchall()
    if len(fetch):
        result = fetch[0][0]
    else:
        result = 0
    #print result
    return (result)


def load_record(connector, cursor, values_dic, db='premier', table='player'):
    global club_names, club_ids
    my_table = '%s_%s' % (db, table)
    if not cursor:
        print 'DB table cursor for %s has not been set up' % my_table
        return (False)
    if not isinstance(values_dic, dict):
        print 'A dictionary of key/value pairs has not been provided or is of the wrong type'
        return (False)
    #print 'club -> %s' % (values_dic['name_club'])
    club_name = unquote(values_dic['name_club'])
    if club_name in club_names:
        values_dic['club_id'] = str(club_names[club_name])
    else:
        print 'Club %s not recognised in DB' % (club_name)
        return (False)
    player_id = player_exists(connector, cursor, values_dic)
    #print 'id: %s' % player_id
    if player_id:
        name = ' '.join([unquote(values_dic['given_name']), unquote(values_dic['surname'])])
        print 'Record for %s at %s already exists' % (name, club_name)
        if unquote(values_dic['given_name']):
            sql = 'UPDATE %s SET given_name = "%s", surname = "%s", squad_number = %s WHERE id_player = %d' % \
                  (my_table, unquote(values_dic['given_name']), unquote(values_dic['surname']), \
                   str(values_dic['squad_number']), int(player_id))
        else:
            sql = 'UPDATE %s SET surname = "%s", squad_number = %s WHERE id_player = %d' % \
                  (my_table, unquote(values_dic['surname']), str(values_dic['squad_number']), int(player_id))
        try:
            cursor.execute(sql)
        except Exception, ex:
            print "Failed to apply SQL '%s'. Reason: %s" % (sql, repr(ex))
            return (False)
        connector.commit()
        return (True)
    del values_dic['name_club']
    columns = ",".join(values_dic.keys())
    for k in values_dic.keys():
        if not isinstance(values_dic[k], int) and not values_dic[k].isdigit() and not quoted(values_dic[k]):
            values_dic[k] = '"%s"' % values_dic[k]
    values = ",".join([values_dic[key] for key in values_dic.keys()])
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
    # test value inserted

    # TODO

    return (True)


def load_records(connector, cursor, filename):
    global clubs
    print 'Loading player records'
    f = open(filename)
    player = f.readline()
    while player:
        player = re.sub('[\n\r]', '', player)
        values = player.split(',')
        #print values
        if len(values) != 4:
            print 'Skipped faulty record "%s"' % player
        else:
            values_dict = {'name_club': values[0],
                           'squad_number': values[1],
                           'surname': values[2],
                           'given_name': values[3]}
            result = load_record(connector, cursor, values_dict)
        player = f.readline()
    # end while
    f.close()


def main(db_name, player_file):
    db_connector, db_cursor = connect_to_db(db_name, file='db.sqlite3')
    if not db_cursor:
        sys.exit(1)
    club_count = select_all_clubs(db_connector, db_cursor)
    print 'Found %d clubs' % club_count
    if load_records(db_connector, db_cursor, player_file):
        sys.exit(0)
    sys.exit(9)


if __name__ == '__main__':
    main('db.sqlite3', sys.argv[1])

