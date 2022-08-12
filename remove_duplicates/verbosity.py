import logging


LOG_LEVELS = ['ERROR', 'INFO', 'DEBUG', 'NOTSET']
DEFAULT_LOG_LEVEL = LOG_LEVELS.index('ERROR')


# todo if vv do timestamps


def init_loglevel(verbosity=DEFAULT_LOG_LEVEL):
    log_level_name = LOG_LEVELS[verbosity]
    logging.getLogger().setLevel(log_level_name)
    logging.debug(f'Beginning deduplication! Logging verbosity = {log_level_name}')
