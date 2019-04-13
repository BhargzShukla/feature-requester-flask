#! venv/bin/python python
import argparse
import json
import os

from flask_fixtures import load_fixtures

from feature_requester_app import app, models

help_message = """
use as - python manage.py [command]

[command] can be replaced by one of the following:

runserver - runs the flask local server

create_db - create the initial database tables

init_db - populate the database with initial data. Make sure to run this
after create_db is run.

drop_db - drop the current database with data
"""

description_message = """
Utility to run various flask commands.
"""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=description_message,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('command', help=help_message)
    args = parser.parse_args()

    if args.command == 'runserver':
        app.run()
    elif args.command == 'create_db':
        models.db.create_all()
    elif args.command == 'drop_db':
        models.db.drop_all()
    elif args.command == 'init_db':
        fixture_dir = os.path.join('feature_requester_app', 'fixtures')
        for fixture in os.listdir(fixture_dir):
            fixture_path = os.path.join(fixture_dir, fixture)
            with open(fixture_path, 'r') as infile:
                load_fixtures(
                    models.db,
                    json.loads(infile.read())
                )
