additional steps:
- do installs before entering virtualenv
- Mkae user/group - useradd groupadd, add self to deployment
- mkdir log file dir and chown/chmod
- (within virtualenv) pip install django==1.3
- (outside virtualenv) pip install uwsgi
- postgres:

sudo apt-get install postgresql libpq-dev
sudo yum install postgresql postgresql-server postgresql-devel
(within virtualenv) easy_install psycopg2

sudo su -
passwd postgres
su - postgres
psql (template1?)
sudo vi /var/lib/pgsql/data/pg_hba.conf
    host    all     all     127.0.0.1/32    trust
CREATE USER progcomp WITH PASSWORD 'progcomp';
CREATE DATABASE progcomp;
GRANT ALL PRIVILEGES ON DATABASE progcomp TO progcomp;

sudo apt-get install memcached
sudo easy_install python-memcached
sudo service memcached start


Setup: http://posterous.adambard.com/start-to-finish-serving-mysql-backed-django-w
uWSGI: http://projects.unbit.it/uwsgi/wiki/Install
Creating accounts: http://www.cyberciti.biz/faq/howto-add-new-linux-user-account/
Add account to group: http://www.cyberciti.biz/faq/howto-linux-add-user-to-group/
Django/PostgreSQL: http://programmingzen.com/2007/12/26/installing-django-with-postgresql-on-ubuntu/
PostgreSQL database: http://www.cyberciti.biz/faq/howto-add-postgresql-user-account/
psycopg: http://initd.org/psycopg/install/
