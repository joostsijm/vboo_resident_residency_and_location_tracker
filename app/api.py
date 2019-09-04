"""API module"""

import re

import requests
from bs4 import BeautifulSoup

from app import BASE_URL, HEADERS

def get_residents(region_id):
    """Get residents from region"""
    return download_players(region_id, 'residency')

def get_citizens(region_id):
    """Get citizens from region"""
    return download_players(region_id, 'state')

def download_players(region_id, player_type):
    """Download the players"""
    players = []
    more = True
    page = 0
    while more:
        response = requests.get(
            '{}listed/{}/{}/0/{}'.format(BASE_URL, player_type, region_id, page*25),
            headers=HEADERS
        )
        tmp_players, more = parse_players(response.text)
        players = players + tmp_players
        page += 1
    return players

def read_citizens():
    """Read from department file"""
    with open('citizens.html') as file:
        citizens = parse_players(file)
        return citizens

def parse_players(html):
    """Parse html return players"""
    soup = BeautifulSoup(html, 'html.parser')
    players_tree = soup.find_all(class_='list_link')
    players = []
    for player_tree in players_tree:
        columns = player_tree.find_all('td')
        players.append({
            'id': int(re.sub(r'^.*\/', '', columns[1]['action'])),
            'name': columns[1].string.strip(),
        })
    more = bool(soup.find(class_='more'))
    return players, more
