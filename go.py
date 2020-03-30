#!/usr/bin/env python3
import os
import click

import pyhmy
from pyhmy import cli as hmy
from pyhmy import Typgpy

import harmony_analytics_ops as ops


def setup():
    assert hasattr(pyhmy, "__version__")
    assert pyhmy.__version__.major == 20, "wrong pyhmy version"
    assert pyhmy.__version__.minor == 1, "wrong pyhmy version"
    assert pyhmy.__version__.micro >= 14, "wrong pyhmy version, update please"
    env = hmy.download("./bin/hmy", replace=False)
    hmy.environment.update(env)
    hmy.set_binary("./bin/hmy")


def dir_check():
    assert os.path.isdir("../jupyter"), "invalid path, check ops dir"
    assert os.path.isdir("../jupyter/logs"), "invalid path, check ops dir"


@click.group()
def cli():
    pass


@cli.command()
@click.option('--count', default=1, help='Number of logs to sync starting from latest')
@click.argument('profile')
def download_logs(profile, count):
    """Download latest logs for a specified profile."""
    logs_dir = ops.find_and_sort_all_logs(profile)
    if len(logs_dir) <= 0:
        print(f"{Typgpy.FAIL}No logs to download.")
        exit(-1)
    if count > len(logs_dir):
        print(f"{Typgpy.FAIL}[Warning] specified count greater than available logs ({len(logs_dir)}).")


if __name__ == "__main__":
    setup()
    dir_check()
    cli()
