from math import log10
from math import pow

LOG_RANGE_DB = 96.0
LOG_OFFSET_DB = 6.0

LOG_OFFSET_VAL = -0.77815125038364363
LOG_RANGE_VAL = -2.00860017176191756


def log_def_to_db(deflection):
    if deflection >= 100.0:
        return 0.0
    if deflection <= 0.0:
        return -100.0
    deflection = deflection / 100
    return (
        -(LOG_RANGE_DB + LOG_OFFSET_DB)
        * pow((LOG_RANGE_DB + LOG_OFFSET_DB) / LOG_OFFSET_DB, -deflection)
        + LOG_OFFSET_DB
    )


def log_db_to_def(db):
    if db >= 0.0:
        return 100.0
    if db <= -96.0:
        return 0.0
    return (
        (-log10(-db + LOG_OFFSET_DB) - LOG_RANGE_VAL) / (LOG_OFFSET_VAL - LOG_RANGE_VAL)
    ) * 100.0
