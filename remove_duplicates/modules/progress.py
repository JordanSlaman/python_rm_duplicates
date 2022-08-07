from collections import defaultdict
import datetime

# Progress
# PROGRESS_GLOBALS = {
#     'total_start_datetime': datetime.datetime.now(),
#     'last_progress_datetime': datetime.datetime.now(),
#     'last_progress_percentage': 0.0,
#     'last_progress_percentage_int': 0,
#
#
#     'tasks': defaultdict(dict)
# }


PROGRESS_INIT_DATETIME = datetime.datetime.now()
PROGRESS_TASKS = defaultdict(dict)

PROGRESS_MINUTES_TO_REPORT = 1
PROGRESS_PERCENTAGE_TO_REPORT = 5

#
# 'total': {
#     'start_datetime': datetime.datetime.now(),
#     'last_progress_percentage': 0.0
# }


def progress(enabled=False, task_str='total', processed_qty=0):
    if enabled:
        task_label = task_str.upper()

        if task_str not in PROGRESS_TASKS.keys():
            PROGRESS_TASKS[task_str] = {
                'start_datetime': datetime.datetime.now(),
                'last_progress_percentage': 0.0
            }

        progress_percentage = int(divmod(0.1, 5)[0])
        x = bool(divmod(10.20, 5)[1])

        if progress_percentage == 0:
            print(progress_percentage)


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
