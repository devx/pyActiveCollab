#import json
import requests
import os
import logging
from pprint import pprint


class activeCollab(object):
    """
    This library interacts with Active Collab 3.x/4.x.
    """

    _USER_NAME = None
    _API_KEY = None
    _URL = None

    def __init__(self, config=None, key=None, user_name=None,
                 url=None, log_level="error", log_file=""):
        """
        Initialize an object to load authentication information and the
        endpoint
        """
        LOGGING_LEVELS = {'critical': logging.CRITICAL,
                          'error': logging.ERROR,
                          'warning': logging.WARNING,
                          'info': logging.INFO,
                          'debug': logging.DEBUG}
        loglevel = LOGGING_LEVELS.get(log_level, logging.NOTSET)

        logging.basicConfig(level=loglevel, filename=log_file,
                            format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing %s" % __name__)

        if config:
            self.load_config(config)
        elif None in (key, user_name, url):
            pprint("We could not set your keys")
        else:
            self._API_KEY = key
            self._USER_NAME = user_name
            self._URL = url

    def load_config(self, config_file):
        """
        Reads and parses a config file that is provided,  If no file path is
        pass it will look for the file in "~/.ActiveCollab".
        """

        import ConfigParser

        try:
            config = ConfigParser.ConfigParser()
            config.readfp(open(os.path.expanduser(config_file)))
            self._API_KEY = config.get('config', 'KEY')
            self._USER_NAME = config.get('config', 'USER')
            self._URL = config.get('config', 'URL')
        except:
            pprint("Could not parse your config file")
            pass

    def call_api(self, ac_method, params=None):
        ac_url = (self._URL + "?auth_api_token=" + self._API_KEY +
                  "&path_info=" + ac_method + "&format=json")

        if params:
            self.logger.info("Requesting call with no parameters")
            self.logger.debug("Calling URL: %s" % ac_url)
        else:
            self.logger.info("Requesting call with no parameters")
            self.logger.debug("Calling URL: %s" % ac_url)
            r = requests.get(str(ac_url))
        return r.text

    def get_info(self):
        """
        Returns system information about the installation you are working with.
        This information includes system versions; info about logged in users;
        the mode the API is in etc.
        """
        return self.call_api('info')

    def get_project_labels(self):
        """
        Lists all available project labels.
        """
        return self.call_api('info/labels/project')
