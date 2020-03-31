import subprocess
import os
import datetime

env = os.environ.copy()
timeout = 120


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
    if f"{profile}/" not in _list_aws_dir("s3://harmony-benchmark/logs/"):
        raise RuntimeError(f"No logs saved for profile `{profile}`")
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


def copy_from_s3(src, dst, recursive=False, include=None, exclude=None,) -> None:
    """
    Copy all files from the given s3 path `src` to the destination path `dst` on the machine.
    One can specify what files to `include` or `exclude` and do a `recursive` copy.
    """
    dst = os.path.abspath(dst)
    os.makedirs(dst, exist_ok=True)
    assert src.startswith('s3://'), f"given source {src} is not an s3 path"
    cmd = ['aws', 's3', 'cp', src, dst]
    if exclude is not None:
        cmd.extend(['--exclude', exclude])
    if include is not None:
        cmd.extend(['--include', include])
    if recursive:
        cmd.append('--recursive')
    subprocess.check_output(cmd, env=env, timeout=timeout).decode().split("\n")
