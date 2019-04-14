# Feature Requester

First, a haiku
> Feature requester\
> letting users create all\
> the feature requests

Feature Requester is a web app that lets users create feature requests. It's developed using Flask,\
SQLAlchemy, jQuery, KnockoutJS and Bootstrap. It uses a custom JSON API that provides CRUD functionality\
for feature requests. The frontend features creation and viewing of features requests.

The app can be deployed on a local machine in 2 ways:

- Using virtualenv
- Using Docker

The virtualenv route is fairly straightforward. There's some configuration required to get things up\
and running. The Docker route is a fully scripted deployment method using the python-3.6 image (built on Debian).\
An instance of the app is currently deployed on Heroku, which you can [check out here.](https://feature-requester-flask.herokuapp.com/)

## Local Deployment

### Virtualenv

- Create a new virtual environment in the project folder
    >$ virtualenv venv
- Activate the virtualenv
    >$ source venv/bin/activate
- Install required packages using pip
    >$ pip install -r requirements.txt
- Create a dotenv file (.env) using the [sample](https://github.com/BhargzShukla/feature-requester-flask/blob/master/.env_sample) provided
    >$ cp .env_sample .env
- Run the following commands to start an app instance
    >$ python manage.py create_db   (creates all required tables in database)\
    >$ python manage.py init_db     (populates those tables with some initial data using flask-fixtures)\
    >$ python manage.py runserver   (calls app.run() with the configuration set in .env)\
- Open [http://localhost:5000](http://localhost:5000) on your favorite browser and get requestin'!
- When you're done, press "Ctrl + C" and then deactivate the virtualenv

### Docker

- Install [Docker](https://docs.docker.com/install/#server) and [Docker Compose](https://docs.docker.com/compose/install/) on your machine
- Make sure ["docker-entrypoint.sh"](https://github.com/BhargzShukla/feature-requester-flask/blob/master/docker-entrypoint.sh) has executable permissions
- Run the following commands to start an app instance
    >$ docker-compose build\
    >$ docker-compose up -d
- Once again, open [http://localhost:5000](http://localhost:5000) on your favorite browser and get requestin'!
- When you're done, you can run
    >$ docker stop `<id>`

## Tests

The project also contains some unittests in [tests.py](https://github.com/BhargzShukla/feature-requester-flask/blob/master/tests.py). These are by no means exhaustive, but merely serve as a starting point. To run them, execute this command in the virtual environment:
>$ python tests.py