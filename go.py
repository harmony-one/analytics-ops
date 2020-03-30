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
    assert os.path.isdir("../jupyter"), "invalid path, check ops dir / working dir"


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
        except NameError:
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
@click.option('--count', default=1, help='Number of logs to download, starting from latest')
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
        assert path.startswith("s3://harmony-benchmark/logs"), f"given source {path} is not a known s3 path"
        path_end = path.replace("s3://harmony-benchmark/logs", "")
        dst = os.path.abspath(f'../jupyter/logs/{path_end}')
        print(f"Copying files from `{path}` to `{dst}`")
        ops.copy_from_s3(path, dst)


@log.command('download-from-path')
@click.argument('path')
def logs_download_from_path(path):
    pass



@click.group()
def notebook():
    """Control all things related to the jupyter notebook files on this machine"""


@notebook.command('protect')
@click.argument('path')
def notebook_protect(path):
    """Make the file or directory readonly"""
    ops.protect(path)
    print(f"Protected `{path}`")


@notebook.command('share')
@click.argument('path')
def notebook_share(path):
    """Make the file or directory writable"""
    ops.share(path)
    print(f"Sharing `{path}`")



if __name__ == "__main__":
    setup()
    dir_check()
    init()
