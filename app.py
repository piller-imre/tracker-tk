from tracker import Tracker
from models import create_database_session


if __name__ == '__main__':
    database_session = create_database_session('sqlite:////tmp/tracker.db')
    Tracker()
