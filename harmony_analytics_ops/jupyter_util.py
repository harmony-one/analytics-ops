import subprocess
import os
import datetime

env = os.environ.copy()
timeout = 120


def protect(path) -> str:
    """
    Make the given `path` readonly.
    """
    cmd = ['chmod', '-w', path]
    return subprocess.check_output(cmd, env=env, timeout=timeout).decode()



