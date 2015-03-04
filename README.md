[![Build Status](https://secure.travis-ci.org/JohanGovers/PertenTime.png?branch=master)](https://travis-ci.org/JohanGovers/PertenTime) [![Coverage Status](https://coveralls.io/repos/JohanGovers/PertenTime/badge.png)](https://coveralls.io/r/JohanGovers/PertenTime)

# PertenTime
This is a project based time reporting system tailored for Perten Instruments HQ. It's made available under GPL v2.



How to install for development

- Download Python3 from https://www.python.org/

git clone https://github.com/JohanGovers/PertenTime.git

cd PertenTime

pip install virtualenvwrapper-win
mkvirtualenv PertenTime
workon PertenTime
setprojectdir .
pip install -r requirements.txt

cd src
python manage.py migrate
python populate_db.py
python manage.py test app
python manage.py runserver


Open http://localhost:8000 in your browser
