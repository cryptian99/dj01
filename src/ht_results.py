#!/usr/bin/python
# __author__ = 'peterhaydon'

# Grab match results from the BBC sports pages

import sys
import requests
from lxml import html

def get_page(page_address):
    try:
        response = requests.get(page_address)
    except Exception, ex:
        print 'HTTP Request failed - %s' % repr(ex)
        return(None)
    return(response.text)

def scrape_page(text_tree):
    pass

def main(args):
    url = args[0]
    web_page = get_page(url)
    #print web_page
    if web_page:
        tree = html.fromstring(web_page)
        useful_data = scrape_page(tree)
    else:
        sys.exit(1)
    print useful_data
    sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])