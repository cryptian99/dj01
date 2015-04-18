#!/usr/bin/python
# __author__ = 'peterhaydon'
from schema import schema, db, goal_default, contribution_default

def get_goals_by_club(club_id):
    pass

def get_goals_by_contribution(connector, contribution_id):
    my_table = goal_default
    sql = "SELECT at_minutes, id_goaltype FROM %s WHERE id_contribution = %s" % \
          (my_table, contribution_id)
    cursor = connector.cursor()
    query = cursor.execute(sql)
    fors = against = 0
    result = cursor.fetchall()
    for goal in result:
        if int(goal[1]) in (0, 1):
            fors += 1
        else:
            against += 1
    return(fors, against)

def goals_by_club_time(connector, club_id):
    my_table = contribution_default
    sql = 'SELECT id_contribution FROM %s WHERE id_club = %s' % (my_table, club_id)
    cursor = connector.cursor()
    query = cursor.execute(sql)
    contributions = cursor.fetchall()
    contribution_list = []
    #print 'found %s contributions' % len(contributions)
    for contribution in contributions:
        contribution_list += [contribution]
    del contributions
    contributors = ','.join(str(contribution[0]) for contribution in contribution_list)
    sql = "SELECT at_minutes, id_goaltype FROM %s WHERE id_contribution IN (%s)" % (goal_default, contributors)
    #print sql
    query = cursor.execute(sql)
    goal_fest = cursor.fetchall()
    #print 'goals found = %s' % len(goal_fest)
    print goal_fest
    # TODO


