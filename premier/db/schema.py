#!/usr/bin/python
# __author__ = 'peterhaydon'

schema = 'db.sqlite3'
db = 'premier'
tables = { 'clubs'         : 'club',
           'players'       : 'player',
           'games'         : 'game',
           'goals'         : 'goal',
           'contributions' : 'contribution',
           'goaltypes'     : 'goaltype'
}
goal_default = '%s_%s' % (db, tables['goals'])
club_default = '%s_%s' % (db, tables['clubs'])
player_default = '%s_%s' % (db, tables['players'])
contribution_default = '%s_%s' % (db, tables['contributions'])
goaltype_default = '%s_%s' % (db, tables['goaltypes'])
game_default = '%s_%s' % (db, tables['games'])


def set_schema(value):
    schema = value

def set_db(value):
    db = value

def make_table_name(table, db=db):
    return('%s_%s' % (db, table))
