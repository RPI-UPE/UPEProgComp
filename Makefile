MANAGE=manage.py
VENV=. env/bin/activate;

venv: env/bin/activate
env/bin/activate: requirements.txt
	[ -d env ] || virtualenv env
	${VENV} pip install -r requirements.txt
	touch env/bin/activate

init: venv
	${VENV} python ${MANAGE} syncdb

update: venv
	${VENV} pip install -U -r requirements.txt

freeze: venv
	${VENV} pip freeze -r requirements.txt > requirements.txt

shell: venv
	${VENV} python ${MANAGE} shell

serve: venv
	${VENV} python ${MANAGE} runserver 0.0.0.0:8000

grade: venv
	${VENV} python ${MANAGE} grade_submissions --traceback
grader: grade

test: venv
	${VENV} python ${MANAGE} test

static: venv
	${VENV} python ${MANAGE} collectstatic --noinput
