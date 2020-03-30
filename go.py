#!/usr/bin/env python3
import click

import pyhmy
from pyhmy import cli as hmy

import harmony_analytics_ops as ops


def setup():
    assert hasattr(pyhmy, "__version__")
    assert pyhmy.__version__.major == 20, "wrong pyhmy version"
    assert pyhmy.__version__.minor == 1, "wrong pyhmy version"
    assert pyhmy.__version__.micro >= 14, "wrong pyhmy version, update please"
    env = hmy.download("./bin/hmy", replace=False)
    hmy.environment.update(env)
    hmy.set_binary("./bin/hmy")


@click.group()
def cli():
    pass


@cli.command()
@cli.argument('profile', help="profile of logs to fetch")
@cli.option('--count', default=1, help='the number of logs to sync starting from latest')
def sync_log(profile, count):
    logs_dir = ops.find_and_sort_all_logs(profile)
    print(logs_dir)


if __name__ == "__main__":
    setup()
    cli()
