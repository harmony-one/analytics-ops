import subprocess
import os

env = os.environ.copy()
timeout = 120


def protect(path) -> None:
    """
    Make the given `path` readonly.
    """
    cmd = ['chattr', '+i', path]
    subprocess.call(cmd, env=env, timeout=timeout)


def share(path) -> None:
    """
    Make the given `path` readonly.
    """
    cmd = ['chattr', '-i', path]
    subprocess.call(cmd, env=env, timeout=timeout)


# TODO: implement publish command.

