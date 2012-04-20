install_dir=/srv/www/
virtual_env=progcomp
user=`logname`
group=deployment

all: 
	-echo "Use `make application' or `make remote'"

# Dependency installation
python:
	yum install python26 python26-devel python-setuptools
virtualenv:
	easy_install virtualenv
postgresql-base:
	yum install postgresql
postgresql-client: postgresql-base python
	yum install postgresql-devel
	easy_install psycopg2
postgresql-server: postgresql-base
	yum install postgresql-server
git: 
	yum install git
server: python
	yum install nginx
	easy_install uwsgi

# Setup
group-setup:
	-useradd uwsgi
	-groupadd ${group}
	useradd -G ${group} uwsgi ${user}

create-root:
	mkdir -p "${install_dir}"
	chown ${user}:${group} "${install_dir}"
	cd "${install_dir}"

create-environment: create-root
	virtualenv --no-site-packages "${virtual_env}"
	cd "${virtual_env}"

application: python virtualenv postgresql-client git server

