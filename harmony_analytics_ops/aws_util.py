import subprocess
import os
import datetime

env = os.environ.copy()
timeout = 60


def _list_aws_dir(directory):
    cmd = ['aws', 's3', 'ls', directory]
    return [n.replace('PRE', '').strip() for n in
            subprocess.check_output(cmd, env=env, timeout=timeout).decode().split("\n") if n]


def find_and_sort_all_logs(profile) -> list:
    """
    Finds all s3 paths for the given `profile`, sorted by most recent date first.

    Note that there is an assumption of the format of the s3 path.
    A valid example (with 'stn' as the profile) is: s3://harmony-benchmark/logs/stn/20/03/30/11:25:58/
    """
    all_logs = []
    init_dir = f"s3://harmony-benchmark/logs/{profile}/"
    year_list = _list_aws_dir(init_dir)
    year_list.sort(key=lambda e: int(e.replace('/', '')), reverse=True)
    for year in year_list:
        year_dir = f'{init_dir}{year}'
        month_list = _list_aws_dir(year_dir)
        month_list.sort(key=lambda e: int(e.replace('/', '')), reverse=True)
        for month in month_list:
            month_dir = f'{year_dir}{month}'
            day_list = _list_aws_dir(month_dir)
            day_list.sort(key=lambda e: int(e.replace('/', '')), reverse=True)
            for day in day_list:
                day_dir = f'{month_dir}{day}'
                time_list = _list_aws_dir(day_dir)
                time_list.sort(key=lambda e: datetime.datetime.strptime(e.replace('/', ''), "%H:%M:%S"), reverse=True)
                for time in time_list:
                    all_logs.append(f'{day_dir}{time}')
    return all_logs


def copy_from_s3(src, dst):
    dst = os.path.abspath(dst)
    os.makedirs(dst, exist_ok=True)
    assert src.startswith('s3://'), f"given source {src} is not an s3 path"
    cmd = ['aws', 's3', 'cp', src, dst, '--recursive']
    subprocess.check_output(cmd, env=env, timeout=timeout).decode().split("\n")
