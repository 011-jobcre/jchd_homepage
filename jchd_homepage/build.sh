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
python manage.py migrate --noinput