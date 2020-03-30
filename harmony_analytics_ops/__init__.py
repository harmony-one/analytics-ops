import sys
import warnings

from .aws_util import (
    find_and_sort_all_logs,
)

if sys.version_info.major < 3:
    warnings.simplefilter("always", DeprecationWarning)
    warnings.warn(
        DeprecationWarning(
            "`harmony_analytics_ops` does not support Python 2. Please use Python 3."
        )
    )
    warnings.resetwarnings()

if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    warnings.simplefilter("always", ImportWarning)
    warnings.warn(
        ImportWarning(
            "`harmony_analytics_ops` does not work on Windows or Cygwin."
        )
    )
    warnings.resetwarnings()
