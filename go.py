#!/usr/bin/env python3
import os
import sys
import click

import pyhmy
from pyhmy import cli as hmy
from pyhmy import Typgpy

import harmony_analytics_ops as ops

env = os.environ.copy()


def setup():
    assert hasattr(pyhmy, "__version__")
    assert pyhmy.__version__.major == 20, "wrong pyhmy version"
    assert pyhmy.__version__.minor == 1, "wrong pyhmy version"
    assert pyhmy.__version__.micro >= 14, "wrong pyhmy version, update please"
    env = hmy.download("./bin/hmy", replace=False)
    hmy.environment.update(env)
    hmy.set_binary("./bin/hmy")


def dir_check():
    """Checks for correct assumptions made by CLI"""
    # assert os.path.isdir("../jupyter"), "invalid path, check ops dir / working dir"
    # assert os.path.isdir("../jupyter/logs"), "invalid path, check ops dir / working dir"


def init():
    root_help_str = """
    Harmony Analytics Machine CLI
    
    Root Commands:      Description:
    
    log <Params>       Control all things related to logs on this machine
    notebook <Params>   Control all things related to the jupyter notebook 
                        files on this machine
    """

    if len(sys.argv) >= 2:
        cmd = sys.argv.pop(1)
        try:
            eval(f"{cmd}(prog_name='go.py {cmd}')")
        except Exception:  # Catch all to print help message under any error
            print(f"{cmd} is an unknown command")
            print(root_help_str)
            exit(-1)
    else:
        print(root_help_str)
        exit(-1)


@click.group()
def log():
    """Control all things related to logs on this machine"""


@log.command('download')
@click.option('--count', default=1, help='Number of logs to sync starting from latest')
@click.argument('profile')
def logs_download(profile, count):
    """Download latest logs for a specified profile."""
    logs_dir = ops.find_and_sort_all_logs(profile)
    if len(logs_dir) <= 0:
        print(f"{Typgpy.FAIL}No logs to download.{Typgpy.ENDC}")
        exit(-1)
    if count > len(logs_dir):
        print(f"{Typgpy.FAIL}[Warning] specified count greater than available logs ({len(logs_dir)}).{Typgpy.ENDC}")
    for path in logs_dir[:count]:
        assert path.startwith("s3://"), f"given source {path} is not an s3 path"
        path_end = [el for el in path.split('/') if el][-1]
        dst = f'../jupyter/logs/{path_end}'
        print(f"Copying files from `{path}` to `{dst}`")
        ops.copy_from_s3(path, dst)


@click.group()
def notebook():
    """Control all things related to the jupyter notebook files on this machine"""


if __name__ == "__main__":
    setup()
    dir_check()
    init()
