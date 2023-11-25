import os

RUN_ENV = os.environ.get('RUN_ENV', 'cloud')
PACKAGE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(PACKAGE_DIR, "data")
TMP_PATH = os.environ.get('TMP_PATH', "/tmp/data")
TMP_LEADERBOARD_PATH = DATA_PATH if RUN_ENV == 'local' else TMP_PATH
TESTING = bool(os.environ.get('TESTING'))
