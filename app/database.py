"""Database module"""

from datetime import datetime

from app import session
from app.models import State, Region, Player, StateRegion, PlayerLocation, PlayerResidency


def get_state_regions(state_id):
    """Get regions from state"""
    state = session.query(State).get(state_id)
    regions = state.regions.filter(StateRegion.until_date_time == None).all()
    return regions

def save_citizens(region_id, citizens):
    """Save citizens to database"""
    for player_dict in citizens:
        player = session.query(Player).get(player_dict['id'])
        if player is None:
            player = Player()
            player.id = player_dict['id']
            player.name = player_dict['name']
            session.add(player)
            session.commit()
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
                    .filter(PlayerLocation.region_id == last_region.id).first()
                old_player_location.until_date_time = datetime.now()
                session.commit()

def save_residents(region_id, residents):
    """Save residents to database"""
    for player_dict in residents:
        player = session.query(Player).get(player_dict['id'])
        if player is None:
            player = Player()
            player.id = player_dict['id']
            player.name = player_dict['name']
            session.add(player)
            session.commit()
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
                    .filter(PlayerResidency.region_id == last_residency.id).first()
                old_player_residency.until_date_time = datetime.now()
                session.commit()
