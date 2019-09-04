"""Main app"""

import time

from app import scheduler, session
from app.api import get_citizens, get_residents
from app.database import get_state_regions # , save_citizens, save_residents


def print_players(players):
    """Print professors"""
    for player in players:
        print('{:20} {:30}'.format(
            player['id'],
            player['name'],
        ))

def job_update_citizens(state_id):
    """Update citizens"""
    regions = get_state_regions(state_id)
    for region in regions:
        citizens = get_citizens(region.id)
        print_players(citizens)
        # save_citizens(citizens)

def job_update_residents(state_id):
    """Update residents"""
    regions = get_state_regions(state_id)
    for region in regions:
        residents = get_residents(region.id)
        print_players(residents)
        # save_citizens(citizens)


def add_update_department(state_id):
    """Add jobs"""
    scheduler.add_job(
        job_update_citizens,
        'cron',
        args=[state_id],
        id='citizens_{}'.format(state_id),
        replace_existing=True,
        minute='0'
    )

if __name__ == '__main__':
    # jobs
    # job_update_citizens(2788)
    job_update_residents(2788)

    # Verenigde Nederlanden
    add_update_department(2788)
    # Belgium
    add_update_department(2604)
    # De Provincien
    add_update_department(2620)

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print('Exiting application')
        session.close()
        exit()
