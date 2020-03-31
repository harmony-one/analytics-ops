#!/usr/bin/env python3
import os
import sys
import click

import pyhmy
from pyhmy import cli as hmy
from pyhmy import Typgpy

import harmony_analytics_ops as ops

env = os.environ.copy()
file_dir = os.path.dirname(os.path.realpath(__file__))


def setup():
    # hmy cli currently not used, but piped for future use.
    assert hasattr(pyhmy, "__version__")
    assert pyhmy.__version__.major == 20, "wrong pyhmy version"
    assert pyhmy.__version__.minor == 1, "wrong pyhmy version"
    assert pyhmy.__version__.micro >= 14, "wrong pyhmy version, update please"
    env = hmy.download(f"{file_dir}/bin/hmy", replace=False)
    hmy.environment.update(env)
    hmy.set_binary(f"{file_dir}/bin/hmy")


def dir_check():
    """Checks for correct assumptions made by CLI"""
    assert os.path.isdir(f"{file_dir}/../jupyter"), "notebook directory is unknown"


def init():
    root_help_str = """
    Harmony Analytics Machine CLI
    
    Root Commands:      Description:
    
    log <Params>       Control all things related to logs on this machine
    notebook <Params>  Control all things related to the jupyter notebook 
                       files on this machine
    """

    if len(sys.argv) >= 2:
        cmd = sys.argv.pop(1)
        try:
            eval(f"{cmd}(prog_name='ops.py {cmd}')")
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
    """Download latest logs for a specified profile"""
    logs_dir = ops.find_and_sort_all_logs(profile)
    if len(logs_dir) <= 0:
        print(f"{Typgpy.FAIL}No logs to download.{Typgpy.ENDC}")
        exit(-1)
    if count > len(logs_dir):
        print(f"{Typgpy.FAIL}[Warning] specified count greater than available logs ({len(logs_dir)}).{Typgpy.ENDC}")
    for path in logs_dir[:count]:
        assert path.startswith("s3://harmony-benchmark/logs"), f"given source {path} is not a known s3 path"
        path_end = path.replace("s3://harmony-benchmark/logs", "")
        dst = os.path.abspath(f'{file_dir}/../jupyter/logs/{path_end}')
        print(f"Copying files from `{path}` to `{dst}`")
        ops.copy_from_s3(path, dst, recursive=True)


@log.command('download-from-path')
@click.option('--recursive/--no-recursive', default=True)
@click.option('--include', default=None, help='Files to include in copy', type=str)
@click.option('--exclude', default=None, help='Files to NOT include in copy', type=str)
@click.argument('path')
def logs_download_from_path(path, recursive, include, exclude):
    """Download logs from a specified path"""
    assert path.startswith("s3://harmony-benchmark/logs"), f"given source {path} is not a known s3 path"
    path_end = path.replace("s3://harmony-benchmark/logs", "")
    dst = os.path.abspath(f'{file_dir}/../jupyter/logs/{path_end}')
    print(f"Copying files from `{path}` to `{dst}`")
    ops.copy_from_s3(path, dst, recursive=recursive, include=include, exclude=exclude)


@click.group()
def notebook():
    """Control all things related to the jupyter notebook files on this machine"""
    if os.geteuid() != 0:
        print(f"{Typgpy.FAIL}Not running as root, exiting...{Typgpy.ENDC}")
        exit(-1)


@notebook.command('protect-path')
@click.argument('path')
def notebook_protect_path(path):
    """Make the file or directory readonly"""
    ops.protect(path)
    print(f"Protected `{path}` (immutable file)")


@notebook.command('protect')
@click.argument('name')
def notebook_protect(name):
    """Protects all notebooks with the given name"""
    directory = os.path.abspath(f"{file_dir}/../jupyter")
    protected_count = 0
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".ipynb") and (name == file or file.replace(".ipynb", "") == name):
                path = os.path.join(subdir, file)
                ops.protect(path)
                print(f"Protected `{path}` (immutable file)")
                protected_count += 1
    print(f"Protected {protected_count} files.")


@notebook.command('share-path')
@click.argument('path')
def notebook_share_path(path):
    """Make the file or directory writable"""
    ops.share(path)
    print(f"Sharing `{path}` (can edit file)")


@notebook.command('share')
@click.argument('name')
def notebook_share(name):
    """Share all notebooks with the given name"""
    directory = os.path.abspath(f"{file_dir}/../jupyter")
    share_count = 0
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".ipynb") and (name == file or file.replace(".ipynb", "") == name):
                path = os.path.join(subdir, file)
                ops.share(path)
                print(f"Sharing `{path}` (can edit file)")
                share_count += 1
    print(f"Shared {share_count} files.")


@notebook.command('publish')
@click.argument('name')
def notebook_publish(name):
    """Publish all notebooks with the given name"""
    directory = os.path.abspath(f"{file_dir}/../jupyter")
    publish_count = 0
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".ipynb") and (name == file or file.replace(".ipynb", "") == name):
                path = os.path.join(subdir, file)
                if input(f"Publish: `{path}`?\n> ") in {'Y', 'y', 'yes', 'Yes'}:
                    raise RuntimeError("Not yet implemented")
                    # TODO: implement publish command in harmony_analytics_ops
                    publish_count += 1
    print(f"Published {publish_count} files.")


if __name__ == "__main__":
    setup()
    dir_check()
    init()
