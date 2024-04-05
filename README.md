# Planetarium-API-Service

API Planetarium is a comprehensive and intuitive platform designed to explore, 
discover, and understand the vast universe of APIs, written on DRF.

###Features
* Reservation Management: Manage reservations for planetarium shows, allowing users to book seats and view their reservation details.
* Ticketing System: Handle ticket sales and distribution for planetarium shows, providing options for purchasing tickets online.
* Show Sessions: View schedules and timings for planetarium shows, including upcoming sessions, show durations, and availability.
* Show Themes: Explore different themes for planetarium shows.
* Planetarium Dome Configuration: Access configuration settings for the planetarium dome.

### To install via GitHub, run the following commands: 
Install PostGreSQL and create db.
```
git clone https://github.com/NPovashevych/Planetarium-API-Service.git
cd Planetarium-API-Service
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
set DB_HOST = <your db host>
set DB_NAME = <your db name>
set DB_USER = <your db user>
set DB_PASSWORD = <your db password>
set SECRET_KEY = <your secret key>
python manage.py migrate
python manage.py runserver
```

### To install via Docker: 
Install Docker.
```
docker-compose build
docker-compose up
```
### Getting access:
* create user via /api/user/register/
* get access token via /api/user/token/
