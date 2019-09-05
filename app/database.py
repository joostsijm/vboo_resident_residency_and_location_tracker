"""Database module"""

from datetime import datetime

from app import session
from app.models import State, Player, StateRegion, \
     PlayerLocation, PlayerResidency, StateWorkPermit


def get_state_regions(state_id):
    """Get regions from state"""
    state = session.query(State).get(state_id)
    return state.regions.filter(StateRegion.until_date_time == None).all()

def save_citizens(region_id, citizens):
    """Save citizens to database"""
    for player_dict in citizens:
        player = session.query(Player).get(player_dict['id'])
        if player is None:
            player = save_player(player_dict)
        last_region = player.locations.first()
        if not last_region or last_region.id != region_id:
            player_location = PlayerLocation()
            player_location.player_id = player.id
            player_location.region_id = region_id
            player_location.from_date_time = datetime.now()
            session.add(player_location)
            session.commit()
            if last_region:
                old_player_location = session.query(PlayerLocation) \
                    .filter(PlayerLocation.player_id == player.id) \
                    .filter(PlayerLocation.region_id == last_region.id) \
                    .order_by(PlayerLocation.from_date_time.desc()).first()
                old_player_location.until_date_time = datetime.now()
                session.commit()

def save_residents(region_id, residents):
    """Save residents to database"""
    for player_dict in residents:
        player = session.query(Player).get(player_dict['id'])
        if player is None:
            player = save_player(player_dict)
        last_residency = player.residencies.first()
        if not last_residency or last_residency.id != region_id:
            player_location = PlayerResidency()
            player_location.player_id = player.id
            player_location.region_id = region_id
            player_location.from_date_time = datetime.now()
            session.add(player_location)
            session.commit()
            if last_residency:
                old_player_residency = session.query(PlayerResidency) \
                    .filter(PlayerResidency.player_id == player.id) \
                    .filter(PlayerResidency.region_id == last_residency.id) \
                    .order_by(PlayerResidency.from_date_time.desc()).first()
                old_player_residency.until_date_time = datetime.now()
                session.commit()


def save_work_permits(state_id, work_permits):
    """Save residents to database"""
    for player_dict in work_permits:
        player = session.query(Player).get(player_dict['id'])
        if player is None:
            player = save_player(player_dict)
        last_work_permit = player.state_work_permits.first()
        if not last_work_permit or last_work_permit.id != state_id:
            state_work_permit = StateWorkPermit()
            state_work_permit.player_id = player.id
            state_work_permit.state_id = state_id
            state_work_permit.from_date_time = player_dict['from']
            session.add(state_work_permit)
            session.commit()
            if last_work_permit:
                old_state_work_permit = session.query(StateWorkPermit) \
                    .filter(StateWorkPermit.player_id == player.id) \
                    .filter(StateWorkPermit.state_id == last_work_permit.id) \
                    .order_by(StateWorkPermit.from_date_time.desc()).first()
                old_state_work_permit.until_date_time = datetime.now()
                session.commit()

def save_player(player_dict):
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
