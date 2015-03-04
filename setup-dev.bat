rem How to install for development

rem - Download Python3 from https://www.python.org/

rem git clone https://github.com/JohanGovers/PertenTime.git

rem cd PertenTime

pip install virtualenvwrapper-win
mkvirtualenv PertenTime
workon PertenTime
setprojectdir .
pip install -r requirements.txt 

cd src
python manage.py migrate
python populate_db.py
rem - run pyhton manage.py test app
python manage.py runserver

rem 
rem - Open http://localhost:8000 in your browser
rem 

