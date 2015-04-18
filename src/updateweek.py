'''
Created on Aug 18, 2014

@author: peterhaydon
'''
#Process the CSV files for one or more weeks
#Each record contains the following columns:
#    1   week number
#    2   match date (YYYYMMDD)
#    3   match kick-off (HHMM)
#    4   home team name
#    5   home team squad number
#    6   player start time (0=unused sub, 1=starter, n=sub)
#    7   player end time (0=unused sub, n=subbed, 90=completed match)
#    8   goal score time
#    9   yellow card count
#    10  red card count
#    11  away team name
#    12  away team squad number
#    13  player start time (0=unused sub, 1=starter, n=sub)
#    14  player end time (0=unused sub, n=subbed, 90=completed match)
#    15  goal score time
#    16  yellow card count
#    17  red card count
        
import os, sys, re

def main(args):
    fname = args[0]
    if not os.access(fname, os.R_OK):
        print 'Cannot find file "%s" - check the filesystem' % fname
        sys.exit(2)
    valid = 0
    with open(fname, "r") as f_in:
        lines = f_in.readlines()
        for line in lines:
            line = re.sub("[\r\n]", "", line)
            tokens = line.split(',')
            if len(tokens) != 17:
                print 'Invalid line "%s" ignored' % line
            else:
                valid += 1
                print 'Looks like a valid record #%d' % valid

    print "Input file processing completed"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Mandatory parameter (input file name) is missing'
        sys.exit(1)
    main(sys.argv[1:])
