##Task
This RESTful movie list management API is implemented in Python 3.7.
The record has the following fields: id, title, year, director, length, rating.
The following functionality has been implemented:
methods GET, POST, PUT, DELETE;
checking the value of the field year <2100;
the existence of a filled title field;
an error is processed when trying to DELETE a missing record.

##Operating procedure 
1. Create a database using SQL Shell (psql).
2. We create environment variables FLASK_CONFIG and, for example, DEV_DATABASE_URL for development mode 
\movie-App> set FLASK_CONFIG = “config.DevelopmentConfig” 
\movie-App> set DEV_DATABASE_URL = 'postgresql: // user: PASSWORD @ localhost / dbname'. 
3. Run the local server:
 \movie-App> manage.py runserver.
4. We make a request for a record with number 3:
\movie-App> http GET http://127.0.0.1:5000/api/v1.0/movies/3.

© Vadim Stetsenko 2020

