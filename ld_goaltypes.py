#
#
#	Load goal types table
#
import os, sys

INCREMENT = 1
DECREMENT = 0

goal_types = { 0: ('Goal', '', INCREMENT),
		1: ('Penalty', 'p', INCREMENT),
		2: ('Own Goal', 'o', DECREMENT) }

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

def load_record(connector, cursor, values_dic, db='premier', table='goaltype'):
	my_table = '%s_%s' % (db, table)
	if not cursor:
		print 'DB table cursor for %s has not been set up' % my_table
		return(False)
	if not isinstance(values_dic, dict):
		print 'A dictionary of key/value pairs has not been provided or is of the wrong type'
		return(False)
	columns = ",".join(values_dic.keys())
	for k in values_dic.keys():
		if not isinstance(values_dic[k], int):
			if not values_dic[k].isdigit():
				values_dic[k] = '"%s"' % values_dic[k]
		else:
			values_dic[k] = str(values_dic[k])
	values = ",".join([values_dic[key] for key in values_dic.keys()])
	sql = 'INSERT INTO %s (%s) VALUES (%s)' % (my_table, columns, values)
	#print sql
	try:
		cursor.execute(sql)
	except Exception, ex:
		if 'not unique' in repr(ex):
			print 'A record for %s already exists. Ignored.' % (values.split(',')[0])
			return(True)
		else:
			print 'Unable to insert record into %s. Reason "%s"' % (my_table, repr(ex))
			return(False)
	connector.commit()
	# test value inserted

	# TODO

	return(True)

def load_records(connector, cursor):
	global goal_types
	print 'Loading goal_type records'
	for goal_type_id in goal_types.keys():
		dict = {'id_goaltype': goal_type_id}
		dict['desc_goaltype'] = goal_types[goal_type_id][0]
		dict['marker_goaltype'] = goal_types[goal_type_id][1]
		dict['increment_goaltype'] = goal_types[goal_type_id][2]
		result = load_record(connector, cursor, dict)
		if not result:
			break
	
def main(db_name):
	db_connector, db_cursor = connect_to_db(db_name, file='db.sqlite3')
	if not db_cursor:
		sys.exit(1)
	if load_records(db_connector, db_cursor):
		sys.exit(0)
	sys.exit(9)

if __name__ == '__main__':
	main('db.sqlite3')

