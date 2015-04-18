#!/usr/bin/python

import sys
import sqlite3

club_ids = []
club_names = []

scorers = []

def get_team_members(connector, club_id, db='premier', table = 'player'):
	my_table = '%s_%s' % (db, table)
	cursor = connector.cursor()
	sql = "SELECT id_player, squad_number, surname FROM %s WHERE club_id = %s ORDER BY squad_number" % \
		(my_table, club_id)
	cursor.execute(sql)
	query = cursor.fetchall()
	for q in query:
		print q
	return(query)

def main():
	connector = sqlite3.connect('db.sqlite3')
	for i in range(1,21):
		get_team_members(connector, i)
	sys.exit(0)

if __name__ == '__main__':
	main()

