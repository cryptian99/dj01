from django.shortcuts import render, render_to_response
#from django.http import HttpResponse
#from django.template.loader import get_template
#from django.template import Context
from premier.db.schema import schema, db, tables
from dj01.settings import STATIC_URL, STATICFILES_DIRS
from premier.db.club import get_clubs, get_club_data, get_result_data, get_player_data, get_club_name
from premier.db.game import get_club_fixtures, get_game_by_id, get_game_by_team_week


# Create your views here.

def show_teams(request):
    result = get_clubs()
    title = 'English Premiership Teams'
    if result and len(result):
        for idx in range(len(result)):
            result[idx] = list(result[idx]) + \
                          [ str('/club/%d/' % (result[idx][0])), \
                            str('/result/%d/' % (result[idx][0])), \
                            str('/fixture/%d/' % (result[idx][0])),\
                            str('/teamstats/%d/' % (result[idx][0]))]
        return(render_to_response('list_teams.html', {'title':title, 'teams':result}))
    return(render_to_response('no_teams.html'))


def show_club(request, club_id):
    result = get_club_data(club_id)
    print result
    title = '%s Players' % result['club'][0]
    players = result['player']
    return(render_to_response('list_players.html', {'title':title, 'players':players}))

def show_team_stats(request, club_id):
    return(render_to_response('under_construction.html'))

def show_full_table(request):
    return(render_to_response('under_construction.html'))

def show_player(request, club_id, squad_number):
    result = get_player_data(club_id, squad_number)
    print 'show_player', result
    player = result['player']
    title = 'View %s Player: %s' % (result['club'], ' '.join([result['player'][3],result['player'][2]]))
    game_data = []
    if result['games']:
        for game in result['games']:
            game_info = get_game_by_id(game[1])
            if game_info:
                game_data += [game_info]
    print 'game_data:', game_data
    return(render_to_response('show_player.html', {'title':title, 'player':player, 'games':game_data}))

def edit_player(request, club_id, squad_number):
    result = get_player_data(club_id, squad_number)
    title = 'Edit %s : %s' % (result['club'], ' '.join(result['player'][2:3]))
    return(render_to_response('show_player.html', {'title':title, 'player':result}))

def delete_player(request, club_id, squad_number):
    result = get_player_data(club_id, squad_number)
    title = 'Delete %s : %s' % (result['club'], ' '.join(result['player'][2:3]))
    return(render_to_response('show_player.html', {'title':title, 'player':result}))

def build_summary(club_name, results):
    win = draw = lose = fors = against = diff = points = 0
    for result in results:
        if club_name == result[2]:
            fors += int(result[4])
            against += int(result[5])
        else:
            fors+= int(result[5])
            against += int(result[4])
        if result[8] == 'W':
            win += 1
        elif result[8] == 'D':
            draw += 1
        else:
            lose += 1
        points += int(result[7])
    if fors > against:
        diff = '+%s' % str(fors - against)
    else:
        diff = fors - against
    return([win, draw, lose, fors, against, diff, points])

def show_results(request, club_id):
    club_name, result = get_result_data(club_id)
    #print 'show_results: %s' % result
    print STATICFILES_DIRS
    title = '%s Results' % club_name
    if result and len(result):
        summary = build_summary(club_name, result['result'])
        return(render_to_response('list_results.html', {'title':title, 'results': result['result'], 'summary':summary }))
    return(render_to_response('no_results.html'))

def show_fixtures(request, club_id):
    stuff = get_club_fixtures(club_id)
    title = '%s Fixtures' % get_club_name(club_id)
    return(render_to_response('list_fixtures.html', {'title':title, 'fixtures':stuff}))
