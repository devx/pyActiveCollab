from ac import activeCollab

__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)
__author__ = "Victor Palma"
__all__ = [
    activeCollab,
]


class APIException(Exception):
    """APIExceptions."""
