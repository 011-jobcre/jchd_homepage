#!/usr/bin/env bash

# Install Python deps
pip install -r requirements.txt

# Install Node deps + build Tailwind
# cd theme
# npm install
# npm run build
# cd ..

# Django collect static
python manage.py collectstatic --noinput --clear
# Migrate database
python manage.py migrate --noinput
# Create superuser
if [[ $CREATE_SUPERUSER == "true" ]]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput
fi