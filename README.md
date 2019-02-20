# flaskr2

#### Description
A mysql powered thumble blog application

#### Why to use Flaskr2?
Though Flaskr is a famous programme introduced by the official tutorial, I
met some problem when I installed it in Python 3.x. I found that it points
to the sqlite3: something was wrong when you didn't install libsqlite-devel
before you compile python. May be you can use yum or apt-get to solve this
problem easily, but if you can't use them by chance? In that case, you have
to install libsqlite-devel manually. I felt a little depressed when I
downloaded the rpm file, typed the rpm command to try to install it, the
system told me that I have to install several dependent packages.

Now you can use flaskr2 instead of flaskr to study flask, forget the sqlite, enjoy mysql.


#### How to run it

- edit the configuration in the flaskr2.py file or export an FLASKR_SETTINGS environment variable pointing to a configuration file.

- Instruct flask to use the right application
   - `#export FLASK_APP=flaskr2.py`
   - `#export FLASK_ENV=development`

- initialize the database with this command:
   - `#flask initdb`
   - `#python2.7 -m flask initdb`

- now you can run flaskr2:
   - `#flask run`
   - `#python2.7 -m flask run`

 the application will greet you on
 http://localhost:5000/ OR
 http://127.0.0.1:5000/