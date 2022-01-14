from configparser import ConfigParser

PARSER = ConfigParser()
PARSER.read('config.ini')

DREMIO = 'options.dremio'


# [options.dremio]
def get_dremio_connection() -> str:
    return PARSER.get(DREMIO, 'connection')


def get_dremio_user() -> str:
    return PARSER.get(DREMIO, 'user')


def get_dremio_password() -> str:
    return PARSER.get(DREMIO, 'password')
