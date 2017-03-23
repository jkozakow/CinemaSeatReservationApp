# Appcinema
Real-time booking app using websockets (Pusher.com)

## Setup

### Docker

If you have a docker host, you can simply use `docker-compose` to build the example, then open [http://localhost:8000]:

```
docker-compose up
```

### Manual

0. Setup virtualenv

        virtualenv -p python3 myenv
        ./myenv/bin/activate

1. Install Python Requirements

        pip install -r requirements.txt
        python setup.py develop

2. Install Bower + Grunt

		npm install -g grunt-cli bower

3. Install Assets

        npm install
        bower install

4. Compile Assets

        grunt

5. Migrate
        ./manage.py migrate

6. Run the Server

        ./manage.py runserver


## Additional technologies

Celery + RabbitMQ


## TO DO

Constrain seat selection:

Seats one-by-one and maximum of 5 in single booking. Unable to leave one-seat space.

Refactoring