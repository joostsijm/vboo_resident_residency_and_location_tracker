"""Main app"""

import time

from app import scheduler, session, LOGGER
from app.api import get_citizens, get_residents
from app.database import get_state_regions, save_citizens, save_residents


def print_players(players):
    """Print professors"""
    for player in players:
        print('{:20} {:30}'.format(
            player['id'],
            player['name'],
        ))

def job_update_citizens(state_id):
    """Update citizens"""
    LOGGER.info('Run update citizens for state "%s"', state_id)
    regions = get_state_regions(state_id)
    for region in regions:
        LOGGER.info('"%s": get citizens', region.name)
        citizens = get_citizens(region.id)
        LOGGER.info('"%s": "%s" citizens', region.name, len(citizens))
        # print_players(citizens)
        save_citizens(region.id, citizens)
        LOGGER.info('"%s": done saving citizens', region.name)

def job_update_residents(state_id):
    """Update residents"""
    LOGGER.info('Run update residents for state "%s"', state_id)
    regions = get_state_regions(state_id)
    for region in regions:
        LOGGER.info('"%s": get residents', region.name)
        residents = get_residents(region.id)
        LOGGER.info('"%s": "%s" residents ', region.name, len(residents))
        # print_players(residents)
        save_residents(region.id, residents)
        LOGGER.info('"%s": done saving residents', region.name)


def add_update_citizens(state_id):
    """Add jobs"""
    scheduler.add_job(
        job_update_citizens,
        'cron',
        args=[state_id],
        id='citizens_{}'.format(state_id),
        replace_existing=True,
        hour='1,3,5,7,9,11,13,15,17,19,21,23'
    )

def add_update_residents(state_id):
    """Add jobs"""
    scheduler.add_job(
        job_update_residents,
        'cron',
        args=[state_id],
        id='residents_{}'.format(state_id),
        replace_existing=True,
        hour='1,7,13,19'
    )


if __name__ == '__main__':
    # jobs
    # job_update_citizens(2788)
    # job_update_residents(2788)

    # Verenigde Nederlanden
    add_update_citizens(2788)
    add_update_residents(2788)
    # Belgium
    add_update_citizens(2604)
    add_update_residents(2604)
    # De Provincien
    add_update_citizens(2620)
    add_update_residents(2620)

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print('Exiting application')
        session.close()
        exit()
