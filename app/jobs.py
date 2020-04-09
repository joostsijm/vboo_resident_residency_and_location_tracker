"""Jobs for scheduler module"""

from app import app


def update_citizens(state_ids, region_ids):
    """Update citizens"""
    app.update_citizens(state_ids, region_ids)

def update_residents(state_ids, region_ids):
    """Update residents"""
    app.update_residents(state_ids, region_ids)

def update_work_permits(state_ids):
    """Update work permits"""
    app.update_work_permits(state_ids)
