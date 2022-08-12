from collections import defaultdict
import datetime
import logging
import math

PROGRESS_DATA = {
    'report_percent': 5,
    'report_minutes': 1,

    'enabled': False,
    'tasks': defaultdict(lambda: {
        'start_datetime': datetime.datetime.now(),
        'filecount': 0,
        'last_progress_report_datetime': datetime.datetime.now()
    })
}


def init_progress(enabled=False, total_filecount=0):
    PROGRESS_DATA['enabled'] = enabled
    total_task = PROGRESS_DATA['tasks']['total']
    total_task['filecount'] = total_filecount
    progress_log()


def log_done():
    total_task = PROGRESS_DATA['tasks']['total']
    total_delta = datetime.datetime.now() - total_task['start_datetime']
    logging.debug(f'Done! - Elapsed total time: {human_timedelta(total_delta)}')


def progress_log(task_name='total', qty_processed=0):
    if PROGRESS_DATA['enabled']:
        log_progress = False
        task_data = PROGRESS_DATA['tasks'][task_name]

        # Percentage
        qty_total = task_data['filecount']
        try:
            percentage_float = (qty_processed / qty_total) * 100
        except ZeroDivisionError:
            return 100
        percentage_int = math.floor(percentage_float)
        if percentage_int % PROGRESS_DATA['report_percent'] == 0:
            log_progress = True

        # Elapsed Time
        now = datetime.datetime.now()
        task_last_reported_elapsed_timedelta = now - task_data['last_progress_report_datetime']
        task_total_elapsed_timedelta = now - task_data['start_datetime']
        if task_last_reported_elapsed_timedelta >= datetime.timedelta(minutes=PROGRESS_DATA['report_minutes']):
            log_progress = True

        # Log!
        if log_progress:
            percentage_str = f'{percentage_float:.2%}'
            time_elapsed_total_str = human_timedelta(task_total_elapsed_timedelta)
            # Elapsed task time: {human_timedelta(elapsed)}

            logging.info(f'PROGRESS: - {task_name.title()}: {percentage_str} - {time_elapsed_total_str}')


def human_timedelta(delta):
    d = delta.days
    h, s = divmod(delta.seconds, 3600)
    m, s = divmod(s, 60)

    if not any((d, h, m, s)):
        return '0 seconds'

    labels = ['day', 'hour', 'minute', 'second']
    dhms = ['%s %s%s' % (i, lbl, 's' if i != 1 else '') for i, lbl in zip([d, h, m, s], labels)]
    for start in range(len(dhms)):
        if not dhms[start].startswith('0'):
            break
    for end in range(len(dhms) - 1, -1, -1):
        if not dhms[end].startswith('0'):
            return ', '.join(dhms[start:end + 1])
