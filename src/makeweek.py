'''
Created on Aug 17, 2014
Updated:
    28/09/2014    Add '1' marker for away team starting 11
    28/11/2014    Add '90' for starters and '0,0' for subs
@author: peterhaydon
'''
import os, sys, re

START = 11
BENCH = 7
TEAM = START + BENCH

current_date = None
current_time = None
current_week = None
week_number = None

def close_file(name):
    pass

def start_week(week_no):
    global current_week, week_number
    if current_week:
        current_week.close()
    out_name = 'Premier-Week-%s.csv' % week_no
    current_week = open(out_name, "w")
    week_number = week_no
    print 'start_week : "%s"' % week_number

def start_date(date_string):
    global current_date
    print 'start_date : "%s"' % date_string
    tokens = date_string.split('/')
    current_date = '%s%s%s' % (tokens[2],tokens[1],tokens[0])

def start_time(time_string):
    global current_time
    print 'start_time : "%s"' % time_string
    current_time = time_string

def do_clubs(tokens):
    global current_week, week_number, current_date, current_time
    #print 'do_clubs : "%s"' % tokens
    idx = tokens.index('|')
    home = ' '.join(tokens[0:idx])
    away = ' '.join(tokens[idx+1:])
    #print 'home = "%s", away = "%s"' % (home, away)
    for i in range(0,TEAM):
        if i < START:
            record = '%s,%s,%s,%s,,1,90,,0,0,%s,,1,90,,0,0\n' % (week_number, current_date, current_time, home, away)
        else:
            record = '%s,%s,%s,%s,,0,0,,0,0,%s,,0,0,,0,0\n' % (week_number, current_date, current_time, home, away)
        current_week.write(record)

keywords = { 'WEEK': start_week, 'DATE': start_date, 'TIME' : start_time}

def main(args):
    global current_week
    #print args
    fname  = args[0]
    if not os.access(fname, os.R_OK):
        print 'Cannot find file "%s" - check the filesystem' % fname
        sys.exit(2)
    with open(fname, "r") as f_in:
        lines = f_in.readlines()
        for line in lines:
            line = re.sub("[\r\n]", "", line)
            tokens = line.split()
            if tokens:
                if len(tokens) == 3:
                    if tokens[1] == '=':
                        test = tokens[0].upper()
                        if test in keywords.keys():
                            keywords[test](tokens[2])
                        else:
                            print 'Unrecognised keyword parameter "%s"' % test
                    if tokens[1] == '|':
                        do_clubs(tokens)
                elif '|' in tokens:
                    do_clubs(tokens)
                else:
                    print 'Unrecognised input data "%s"' % line

    print "Input file %s processing completed" % fname
    if current_week:
        current_week.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Mandatory parameter (input file name) is missing'
        sys.exit(1)
    main(sys.argv[1:])


