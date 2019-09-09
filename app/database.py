"""Database module"""

from datetime import datetime

from app import Session
from app.models import State, Player, StateRegion, \
     PlayerLocation, PlayerResidency, StateWorkPermit


def get_state_regions(state_id):
    """Get regions from state"""
    session = Session()
    state = session.query(State).get(state_id)
    regions = state.regions.filter(StateRegion.until_date_time == None).all()
    session.close()
    return regions

def save_citizens(region_id, citizens):
    """Save citizens to database"""
    session = Session()
    player_ids = []
    for player_dict in citizens:
        player = session.query(Player).get(player_dict['id'])
        if player is None:
            player = save_player(session, player_dict)
        player_ids.append(player.id)
        last_region = player.locations.first()
        if not last_region or last_region.id != region_id:
            player_location = PlayerLocation()
            player_location.player_id = player.id
            player_location.region_id = region_id
            player_location.from_date_time = datetime.now()
            session.add(player_location)
    session.commit()
    current_citizens = session.query(PlayerLocation) \
        .filter(PlayerLocation.region_id == region_id) \
        .filter(PlayerLocation.until_date_time == None).all()
    for current_citizen in current_citizens:
        if current_citizen.player_id not in player_ids:
            current_citizen.until_date_time = datetime.now()
    session.commit()
    session.close()


def save_residents(region_id, residents):
    """Save residents to database"""
    session = Session()
    player_ids = []
    for player_dict in residents:
        player = session.query(Player).get(player_dict['id'])
        if player is None:
            player = save_player(session, player_dict)
        player_ids.append(player.id)
        last_residency = player.residencies.first()
        if not last_residency or last_residency.id != region_id:
            player_location = PlayerResidency()
            player_location.player_id = player.id
            player_location.region_id = region_id
            player_location.from_date_time = datetime.now()
            session.add(player_location)
            session.commit()
    current_residents = session.query(PlayerResidency) \
        .filter(PlayerResidency.region_id == region_id) \
        .filter(PlayerResidency.until_date_time == None).all()
    for current_resident in current_residents:
        if current_resident.player_id not in player_ids:
            current_resident.until_date_time = datetime.now()
    session.commit()
    session.close()


def save_work_permits(state_id, work_permits):
    """Save residents to database"""
    session = Session()
    player_ids = []
    for player_dict in work_permits:
        player = session.query(Player).get(player_dict['id'])
        if player is None:
            player = save_player(session, player_dict)
        player_ids.append(player.id)
        last_work_permit = player.state_work_permits.first()
        if not last_work_permit or last_work_permit.id != state_id:
            state_work_permit = StateWorkPermit()
            state_work_permit.player_id = player.id
            state_work_permit.state_id = state_id
            state_work_permit.from_date_time = player_dict['from']
            session.add(state_work_permit)
            session.commit()
    current_work_permits = session.query(StateWorkPermit) \
        .filter(StateWorkPermit.state_id == state_id) \
        .filter(StateWorkPermit.until_date_time == None).all()
    for current_work_permit in current_work_permits:
        if current_work_permit.player_id not in player_ids:
            current_work_permit.until_date_time = datetime.now()
    session.commit()
    session.close()

def save_player(session, player_dict):
    """Save player to database"""
    player = Player()
    player.id = player_dict['id']
    player.name = player_dict['name']
    player.nation = player_dict['nation']
    if 'registration_date' in player_dict:
        player.registration_date = player_dict['registration_date']
    session.add(player)
    session.commit()
    return player
