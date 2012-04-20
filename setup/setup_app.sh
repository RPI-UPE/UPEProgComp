#!/bin/sh

install_dir=/srv/www
virtual_env=progcomp
group=deployment

# ------------------------------------------------------------------------------
# Script init
# ------------------------------------------------------------------------------

# Check root
if [ "$(id -u)" != "0" ]; then
	echo "This script must be run as root" 1>&2
	exit 1
fi

# Get user name
user=$(logname)

# Read command line args
# WARNING: These are largely untested/unimplemented
while [ "$1" != "" ]; do
	case $1 in
		--path )	install_dir=$2
					shift
					;;
		--env  )	virtual_env=$2
					shift
					;;
		--group)	group=$2
					shift
					;;
	esac
	shift
done

# Determine installer
packager=
if ! which yum &>/dev/null; then
	# No yum, check apt-get
	if ! which apt-get &>/dev/null; then
		# Don't know what to do
		echo "Unknown package manager. You must install dependencies yourself."
	else
		packager=apt-get
	fi
else
	packager=yum
fi

# ------------------------------------------------------------------------------
# Check dependencies
# ------------------------------------------------------------------------------

# python26, python26-devel, python-setuptools
yum install python26 python26-devel python-setuptools

# virtualenv
easy_install virtualenv

# postgresql (client side)
yum install postgresql postgresql-devel

# git
yum install git

# nginx, uwsgi
yum install nginx
easy_install uwsgi

# ------------------------------------------------------------------------------
# Install app
# ------------------------------------------------------------------------------

# Create user and group
useradd uwsgi
groupadd $group
useradd -G $group uwsgi $user

# Create directory
mkdir -p "$install_dir"
chown $user:$group "$install_dir"
cd "$install_dir"

# Setup environment
virtualenv --no-site-packages $virtual_env
cd $virtual_env

# Install python packages
source bin/activate
pip install django==1.3 south psycopg2

# Checkout repo and set permissions
git clone https://github.com/jrock08/UPEProgComp/
chmod -R g+w UPEProgComp
cd UPEProgComp

# Setup conf files for nginx and uwsgi
cp setup/conf/nginx.conf /etc/nginx/conf.d/default.conf
cp setup/conf/uwsgi.conf /etc/init/uwsgi.conf


