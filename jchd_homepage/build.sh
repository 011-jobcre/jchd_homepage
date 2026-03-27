#!/usr/bin/env bash

# Install Python deps
pip install -r requirements.txt
# Django collect static
python manage.py collectstatic --noinput --clear
# Migrate database
python manage.py migrate --noinput
# Create superuser
if [[ $CREATE_SUPERUSER == "true" ]]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput
fi