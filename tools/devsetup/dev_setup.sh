#!/bin/bash

set -e

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <hostname> <port> <database> <user>"
    exit
fi

PGH=$1
PGP=$2
PGD=$3
PGU=$4

echo "Host/path to postgres: $PGH"
echo "                 Port: $PGP"
echo "             Database: $PGD"
echo "                 User: $PGU"

echo "Verifying postgres connection..."
psql -w "host=$PGH port=$PGP dbname=$PGD user=$PGU" -c "SELECT 1" >/dev/null

echo "Verifying that pgcrypto is installed in the pgcrypto schema..."
psql -w "host=$PGH port=$PGP dbname=$PGD user=$PGU" -c "CREATE SCHEMA IF NOT EXISTS pgcrypto; CREATE EXTENSION IF NOT EXISTS pgcrypto SCHEMA pgcrypto; SELECT pgcrypto.gen_random_uuid()"

# Start from script directory to be safe!
cd "${0%/*}"

virtualenv --python=python3 venv_dev
venv_dev/bin/pip install -r dev_requirements.txt

cd ../..
cat > postgresqleu/local_settings.py <<EOF
DEBUG=True
DISABLE_HTTPS_REDIRECTS=True
DATABASES={
 'default': {
   'ENGINE': 'django.db.backends.postgresql_psycopg2',
   'NAME': '$PGD',
   'HOST': '$PGH',
   'PORT': '$PGP',
   'USER': '$PGU',
 }
}
SECRET_KEY='reallysecretbutwhocares'
SERVER_EMAIL='root@localhost'
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SITEBASE="http://localhost:8012/"
EOF

tools/devsetup/venv_dev/bin/python manage.py migrate

cat tools/devsetup/devserver-uwsgi.ini.tmpl | sed -e "s#%DJANGO%#$(pwd)/tools/devsetup/venv_dev#g" > devserver-uwsgi.ini

echo ""
echo "Creating a django superuser, and setting password!"
tools/devsetup/venv_dev/bin/python manage.py createsuperuser

echo "All ready to go. To start the development server, go to"
pwd
echo "and run:"
echo "venv_dev/bin/uwsgi --ini devserver-uwsgi.ini"
echo ""
echo "or for a slightly more limited version:"
echo "venv_dev/bin/python manage.py runserver"
