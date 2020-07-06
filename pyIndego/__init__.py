"""Init for Indego class."""
from pkg_resources import DistributionNotFound, get_distribution

try:
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

from .indego_async_client import IndegoAsyncClient
from .indego_client import IndegoClient
