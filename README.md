UPE Prog Comp Server
====================

Requirements
------------
* Python 2.7
* Django 1.3

Installation
------------
The following will create a database and allow you to set up an admin account.
Note: Admin accounts cannot be used on the main website. You must create a
separate profile once the server is running.

    $ cd progcomp
    $ python manage.py syncdb

Running the Server
------------------
The local configuration file `local_settings.py` is used automatically if
present.

    $ cd progcomp
    $ python manage.py runserver

The server can be accessed at <http://127.0.0.1:8000/>.

Administration
--------------
Point your browser to <http://127.0.0.1:8000/admin/>

Directories
-----------
* database: Sqlite3 databases
* grader: Directories for each problem and their sets of inputs and expected
  outputs
* media: Files to be transferred to and received from users
  * output\_file: Program output received from users, referenced by database
  * resumes: PDF/text files of users' resumes, referenced by database
  * sources: Problem results submitted by users with output, referenced by
    database
  * users: Contains hashed directory for each user via which problem inputs will
    be hardlinked from /grader. May also contain diffs from solutions.
* progcomp: Project source
* public:
* static: Static content served, e.g., javascript, css, images
* templates: HTML files loaded by Django's templater
