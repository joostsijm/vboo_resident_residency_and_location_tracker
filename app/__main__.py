"""Main app"""

import time

from app import scheduler, LOGGER
from app.api import get_citizens, get_residents, get_work_permits
from app.database import get_state_regions, save_citizens, save_residents, save_work_permits


def print_players(players):
    """Print professors"""
    for player in players:
        print('{:20} {:30} {:30}'.format(
            player['id'],
            player['name'],
            player['nation'],
        ))

def job_update_citizens(state_id):
    """Update citizens"""
    LOGGER.info('Run update citizens for state "%s"', state_id)
    regions = get_state_regions(state_id)
    for region in regions:
        LOGGER.info('regio %6s: get citizens', region.id)
        citizens = get_citizens(region.id)
        LOGGER.info('regio %6s: "%s" citizens', region.id, len(citizens))
        # print_players(citizens)
        save_citizens(region.id, citizens)
        LOGGER.info('regio %6s: done saving citizens', region.id)

def job_update_residents(state_id):
    """Update residents"""
    LOGGER.info('Run update residents for state "%s"', state_id)
    regions = get_state_regions(state_id)
    for region in regions:
        LOGGER.info('regio %6s: get residents', region.id)
        residents = get_residents(region.id)
        LOGGER.info('regio %6s: "%s" residents ', region.id, len(residents))
        # print_players(residents)
        save_residents(region.id, residents)
        LOGGER.info('regio %6s: done saving residents', region.id)

def job_update_work_permits(state_id):
    """Update citizens"""
    LOGGER.info('state "%s": get work permits ', state_id)
    work_permits = get_work_permits(state_id)
    LOGGER.info('state "%s": "%s" work permits', state_id, len(work_permits))
    # print_players(work_permits)
    save_work_permits(state_id, work_permits)
    LOGGER.info('state "%s": done saving work_permits', state_id)


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

def add_update_work_permits(state_id):
    """Add jobs"""
    scheduler.add_job(
        job_update_work_permits,
        'cron',
        args=[state_id],
        id='work_permits_{}'.format(state_id),
        replace_existing=True,
        hour='4'
    )

if __name__ == '__main__':
    # jobs
    # job_update_citizens(2788)
    # job_update_residents(2788)
    # job_update_work_permits(2788)

    # Verenigde Nederlanden
    add_update_citizens(2788)
    add_update_residents(2788)
    add_update_work_permits(2788)
    # Belgium
    add_update_citizens(2604)
    add_update_residents(2604)
    add_update_work_permits(2604)
    # De Provincien
    add_update_citizens(2620)
    add_update_residents(2620)
    add_update_work_permits(2620)

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        LOGGER.info('Exiting application')
        exit()
