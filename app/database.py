"""Database module"""

from datetime import datetime

from app import SESSION, LOGGER
from app.models import State, Region, Player, StateRegion, \
     PlayerLocation, PlayerResidency, StateWorkPermit


def get_regions(region_ids):
    """Get regions from list"""
    session = SESSION()
    regions = []
    for region_id in region_ids:
        region = session.query(Region).get(region_id)
        if not region:
            region = save_region(session, region_id)
        regions.append(region)
    session.close()
    return regions

def get_state_regions(state_id):
    """Get regions from state"""
    session = SESSION()
    state = session.query(State).get(state_id)
    region_list = []
    if state:
        region_list = state.regions.filter(StateRegion.until_date_time == None).all()
    else:
        save_state(session, state_id)
        LOGGER.error('State %6s: not found', state_id)
    session.close()
    return region_list

def save_citizens(region_id, citizens):
    """Save citizens to database"""
    session = SESSION()
    player_ids = []
    new_citizens = 0
    for player_dict in citizens:
        player = session.query(Player).get(player_dict['id'])
        if player is None:
            player = save_player(session, player_dict)
        player_ids.append(player.id)
        last_location = player.locations \
            .filter(PlayerLocation.region_id == region_id) \
            .filter(PlayerLocation.until_date_time == None) \
            .first()
        if not last_location:
            new_citizens += 1
            player_location = PlayerLocation()
            player_location.player_id = player.id
            player_location.region_id = region_id
            player_location.from_date_time = datetime.now().replace(second=0, minute=0)
            session.add(player_location)
    LOGGER.info('regio %6s: "%s" new citizens', region_id, new_citizens)
    session.commit()
    current_citizens = session.query(PlayerLocation) \
        .filter(PlayerLocation.region_id == region_id) \
        .filter(PlayerLocation.until_date_time == None).all()
    left_citizens = 0
    for current_citizen in current_citizens:
        if current_citizen.player_id not in player_ids:
            left_citizens += 1
            current_citizen.until_date_time = datetime.now().replace(second=0, minute=0)
    LOGGER.info('regio %6s: "%s" citizens left', region_id, left_citizens)
    session.commit()
    session.close()


def save_residents(region_id, residents):
    """Save residents to database"""
    session = SESSION()
    player_ids = []
    new_residents = 0
    for player_dict in residents:
        player = session.query(Player).get(player_dict['id'])
        if player is None:
            player = save_player(session, player_dict)
        player_ids.append(player.id)
        last_residency = player.residencies \
            .filter(PlayerResidency.region_id == region_id) \
            .filter(PlayerResidency.until_date_time == None) \
            .first()
        if not last_residency:
            new_residents += 1
            player_location = PlayerResidency()
            player_location.player_id = player.id
            player_location.region_id = region_id
            player_location.from_date_time = datetime.now().replace(second=0, minute=0)
            session.add(player_location)
    LOGGER.info('regio %6s: "%s" new residents', region_id, new_residents)
    session.commit()
    current_residents = session.query(PlayerResidency) \
        .filter(PlayerResidency.region_id == region_id) \
        .filter(PlayerResidency.until_date_time == None).all()
    for current_resident in current_residents:
        if current_resident.player_id not in player_ids:
            current_resident.until_date_time = datetime.now().replace(second=0, minute=0)
    session.commit()
    session.close()


def save_work_permits(state_id, work_permits):
    """Save residents to database"""
    session = SESSION()
    player_ids = []
    new_work_permits = 0
    for player_dict in work_permits:
        player = session.query(Player).get(player_dict['id'])
        if player is None:
            player = save_player(session, player_dict)
        player_ids.append(player.id)
        last_work_permit = player.state_work_permits \
            .filter(StateWorkPermit.state_id == state_id) \
            .filter(StateWorkPermit.until_date_time == None) \
            .first()
        if not last_work_permit:
            new_work_permits += 1
            state_work_permit = StateWorkPermit()
            state_work_permit.player_id = player.id
            state_work_permit.state_id = state_id
            state_work_permit.from_date_time = player_dict['from']
            session.add(state_work_permit)
    session.commit()
    LOGGER.info('state %6s: "%s" new work permits', state_id, new_work_permits)
    current_work_permits = session.query(StateWorkPermit) \
        .filter(StateWorkPermit.state_id == state_id) \
        .filter(StateWorkPermit.until_date_time == None).all()
    for current_work_permit in current_work_permits:
        if current_work_permit.player_id not in player_ids:
            current_work_permit.until_date_time = datetime.now().replace(second=0, minute=0)
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

def save_state(session, state_id):
    """Save state to database"""
    state = State()
    state.id = state_id
    session.add(state)
    session.commit()
    return state

def save_region(session, region_id):
    """Save region to database"""
    region = Region()
    region.id = region_id
    session.add(region)
    session.commit()
    return region
