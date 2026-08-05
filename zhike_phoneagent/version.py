"""Package version helper."""

from importlib.metadata import version as get_version

try:
    APP_VERSION = get_version("zhike-phoneagent")
except Exception:
    APP_VERSION = "dev"
