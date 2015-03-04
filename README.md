[![Build Status](https://secure.travis-ci.org/JohanGovers/PertenTime.png?branch=master)](https://travis-ci.org/JohanGovers/PertenTime) [![Coverage Status](https://coveralls.io/repos/JohanGovers/PertenTime/badge.png)](https://coveralls.io/r/JohanGovers/PertenTime)

# PertenTime
This is a project based time reporting system tailored for Perten Instruments HQ. It's made available under GPL v2.


## How to install for development
This section guides you step by step on how to install the necessary prerequisites and start the project on windows.

### Prerequisites
First you need to download and install Python3 from https://www.python.org/. You'll also need to install [git](http://git-scm.com/downloads).

Then you're ready to clone this repository. Open a command prompt and run

```
git clone https://github.com/JohanGovers/PertenTime.git
```

#### Setting up virtualenv
Enter the repository and install virtualenv for windows. Then create a new virtualenv for this project, enter it, set the project directory to the root of the repository and install the python packages needed to run the code. All this is done by issueing the following commands.

```
cd PertenTime
pip install virtualenvwrapper-win
mkvirtualenv PertenTime
workon PertenTime
setprojectdir .
pip install -r requirements.txt
```

If you don't want to use virtualenv you must still install the required packages (the last row of the commands above). To enter a virtualenv use ```workon [envname]``` and to exit a virtualenv use ```deactivate```.

### Django setup
PertenTime currently uses sqlite as its database. The database will show up as a file named PertenTime.sqlite3 in the src directory when created. To dump the database simply remove the file.

To create the database change directory to the src folder and run the django migrate command by issuesing the following

```
cd src
python manage.py migrate
```

To get some example test data in your database use
```
python populate_db.py
```

To run the development web server type
```
python manage.py runserver
```

You can then use your development version of PertenTime from http://localhost:8000 in your browser.

### Tutorials
If you want to learn Django fast try [How To Tango With Django 1.7](http://www.tangowithdjango.com/book17/index.html).

