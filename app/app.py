"""General application logic"""

from app import LOGGER, api, database


def print_players(players):
    """Print professors"""
    for player in players:
        print('{:20} {:30} {:30}'.format(
            player['id'],
            player['name'],
            player['nation'],
        ))

def update_citizens(state_ids, region_ids):
    """Update citizens"""
    regions = database.get_regions(region_ids)
    for state_id in state_ids:
        regions += database.get_state_regions(state_id)
    LOGGER.info('update citizens for "%s" regions', len(regions))
    for region in regions:
        LOGGER.info('regio %6s: get citizens', region.id)
        citizens = api.get_citizens(region.id)
        LOGGER.info('regio %6s: "%s" citizens', region.id, len(citizens))
        # print_players(citizens)
        database.save_citizens(region.id, citizens)
        LOGGER.info('regio %6s: done saving citizens', region.id)

def update_residents(state_ids, region_ids):
    """Update residents"""
    regions = database.get_regions(region_ids)
    for state_id in state_ids:
        regions += database.get_state_regions(state_id)
    LOGGER.info('update residents for "%s" regions', len(regions))
    for region in regions:
        LOGGER.info('regio %6s: get residents', region.id)
        residents = api.get_residents(region.id)
        LOGGER.info('regio %6s: "%s" residents ', region.id, len(residents))
        # print_players(residents)
        database.save_residents(region.id, residents)
        LOGGER.info('regio %6s: done saving residents', region.id)

def update_work_permits(state_ids):
    """Update work permits"""
    LOGGER.info('update work permits for "%s" states', len(state_ids))
    for state_id in state_ids:
        LOGGER.info('state %6s: get work permits ', state_id)
        work_permits = api.get_work_permits(state_id)
        LOGGER.info('state %6s: "%s" work permits', state_id, len(work_permits))
        # print_players(work_permits)
        database.save_work_permits(state_id, work_permits)
        LOGGER.info('state %6s: done saving work_permits', state_id)
