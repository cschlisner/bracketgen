# Brackets

[ Brackets ] is a tournament creation and management site. It is built using the Django web framework. 

Users and non-users alike can create new tournaments and add any quantity of participants. Additionally, users from a different device can join and participate in the tournament if they have the tournament's reference code. When starting the tournament, a tournament bracket will generate and the tournament host can choose who wins and loses paired matches, until a final champion is chosen.

The backend software stack is:

#### MySQL - database
#### Django - template management / url mapping / database management / request handling
#### Apache2 - basic http server

------
Directory structure:

brackets/                     (Django Project Dir)

-- brackets/                  (Site Directory)

-- -- urls.py                 (Links brackets & bracketgen folder together)
  
-- -- wsgi.py 

-- bracketgen/                (Main App Directory)

-- -- migrations/

-- -- static/ 

-- -- -- css/ 

-- -- -- -- styles-dark.css   (Main CSS file for whole website)

-- -- -- js/ 

-- -- -- -- tournament.js     (Javascript function for tournament generation)

-- -- -- favicon_16.png

-- -- templates/              (HTML templates)

-- -- -- registration/

-- -- -- base_generic.html    (Base HTML code for rest of templates)

-- -- -- index.html           (Home Page)

-- -- -- my_tournaments.html

-- -- -- signup.html

-- -- -- tournament.html

-- -- -- tournamentform.html

-- -- -- user_info.html

-- -- -- userupdateform.html

-- -- test/                   (Test Cases)

-- -- -- test_forms.py

-- -- -- test_models.py

-- -- __init__.py

-- -- admin.py

-- -- app.py

-- -- forms.py

-- -- models.py 

-- -- urls.py

-- -- views.py

-- manage.py (Python file used to run server & combine file)


## Getting started with development
```
$ git clone https://github.com/garo4938/Bracket-Boys
$ cd Bracket-Boys/
$ pip3 install virtualenv
$ virtualenv bracketsenv
$ source bracketsenv/env/bin/activate
$ pip install django
$ cd brackets/brackets
$ pip install mysqlclient
```


