"""Main app"""

import sys
import time

from app import SCHEDULER, LOGGER, jobs


if __name__ == '__main__':
    LOGGER.info('Starting application')

    # state to track citizens, residents, and work permits
    STATE_IDS = [
        3304, # VN
        3261, # Craftbroec
    ]

    # aditional regions to track citizens and residents
    REGION_IDS = [
        4001, # Noord
        4002, # Oost
        4003, # West
        4004, # Zuid
        4008, # Amsterdam
        4101, # Vlaanderen
        4102, # Walonie
        4103, # Brussel
        200062, # Maan regio 62
    ]

    # jobs
    # jobs.update_citizens(STATE_IDS, REGION_IDS)
    # jobs.update_residents(STATE_IDS, REGION_IDS)
    # jobs.update_work_permits(STATE_IDS)

    # Update citizens
    SCHEDULER.add_job(
        jobs.update_citizens,
        'cron',
        args=[STATE_IDS, REGION_IDS],
        id='update_citizens',
        replace_existing=True,
        hour='1,3,5,7,9,11,13,15,17,19,21,23'
    )
    # Update residents
    SCHEDULER.add_job(
        jobs.update_residents,
        'cron',
        args=[STATE_IDS, REGION_IDS],
        id='residents',
        replace_existing=True,
        hour='1,4,7,10,13,16,19,22'
    )
    # Work permits
    SCHEDULER.add_job(
        jobs.update_work_permits,
        'cron',
        args=[STATE_IDS],
        id='work_permits',
        replace_existing=True,
        hour='2,5,8,11,14,17,20,23'
    )

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        LOGGER.info('Exiting application')
        SCHEDULER.shutdown()
        sys.exit()
