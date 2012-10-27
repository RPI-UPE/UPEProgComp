CD=cd progcomp;
MANAGE=manage.py
VENV=. env/bin/activate;

venv: env/bin/activate
env/bin/activate: requirements.txt
	[ -d env ] || virtualenv env
	${VENV} pip install -r requirements.txt
	touch env/bin/activate

init: venv
	${VENV} ${CD} python ${MANAGE} syncdb

update: venv
	${VENV} pip install -U -r requirements.txt

freeze: venv
	${VENV} pip freeze -r requirements.txt > requirements.txt

serve: venv
	${VENV} ${CD} python ${MANAGE} runserver

grade: venv
	${VENV} ${CD} python ${MANAGE} grade_submissions

test: venv
	${VENV} ${CD} python ${MANAGE} test
