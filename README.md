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

Additionally, once the database is created you must add problems that are placed
in the grader folder via the administration panel (see below).

Running the Server
------------------
The local configuration file `local_settings.py` is used automatically if
present.

    $ cd progcomp
    $ python manage.py runserver

The server can be accessed at <http://127.0.0.1:8000/>.

Running the Grader
------------------
Submissions are not graded by the application. The grader daemon can be started
in the same way the server is and runs in the background alongside it
occasionally querying the database to check for new submissions.

    $ cd progcomp
    $ python manage.py grade_submissions

Administration
--------------
Point your browser to <http://127.0.0.1:8000/admin/>

Directories
-----------
* conf: Sample configuration files for nginx and uWSGI
* database: Sqlite3 databases for use in development
* grader: Directories for each problem and their sets of inputs and expected
  outputs
* media: Files to be transferred to and received from users
  * output\_file: Program output received from users, referenced by database
  * resumes: PDF/text files of users' resumes, referenced by database
  * sources: Problem results submitted by users with output, referenced by
    database
  * users: Directories for each user
    * inputs: A specifically assigned input file from problems will be
      hardlinked to this directory
    * diff: Contains diffs of all failed executions
* progcomp: Project source
* static: Static content served, e.g., javascript, css, images
* templates: HTML files loaded by Django's templater
