"""API module"""

import re
from datetime import datetime, date, timedelta

import requests
from bs4 import BeautifulSoup

from app import BASE_URL, HEADERS

def get_residents(region_id):
    """Get residents from region"""
    return download_players(region_id, 'residency')

def get_citizens(region_id):
    """Get citizens from region"""
    return download_players(region_id, 'region')

def get_work_permits(state_id):
    """Get work permits from state"""
    return download_players(state_id, 'permits_state')

def download_players(region_id, player_type):
    """Download the players"""
    players = []
    more = True
    page = 0
    while more:
        if player_type == 'permits_state':
            url = '{}listed/{}/{}/{}'.format(BASE_URL, player_type, region_id, page*25)
        else:
            url = '{}listed/{}/{}/0/{}'.format(BASE_URL, player_type, region_id, page*25)
        response = requests.get(
            url,
            headers=HEADERS
        )
        if player_type == 'permits_state':
            tmp_players, more = parse_work_permits(response.text)
        else:
            tmp_players, more = parse_players(response.text)
        players = players + tmp_players
        page += 1
    return players

def parse_players(html):
    """Parse html return players"""
    soup = BeautifulSoup(html, 'html.parser')
    players_tree = soup.find_all(class_='list_link')
    players = []
    for player_tree in players_tree:
        columns = player_tree.find_all('td')
        registration_date = parse_date(columns[2].string)
        players.append({
            'id': int(re.sub(r'^.*\/', '', columns[1]['action'])),
            'name': columns[1].string.strip(),
            'nation': columns[5]['title'],
            'registration_date': registration_date
        })
    return players, bool(len(players_tree) >= 25)

def parse_work_permits(html):
    """Parse html return players"""
    soup = BeautifulSoup(html, 'html.parser')
    players_tree = soup.find_all(class_='list_link')
    players = []
    for player_tree in players_tree:
        columns = player_tree.find_all('td')
        registration_date = parse_date(columns[2].string)
        players.append({
            'id': int(columns[1].find(class_='small')['user']),
            'name': columns[1].contents[0].strip(),
            'nation': columns[5]['title'],
            'from': registration_date
        })
    return players, bool(len(players_tree) >= 25)

def parse_date(date_string):
    """Parse date to object"""
    if 'Today' in date_string:
        return date.today()
    if 'Yesterday' in date_string:
        return date.today() - timedelta(1)
    return datetime.strptime(date_string, '%d %B %Y').date()
