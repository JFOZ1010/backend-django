#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
echo "BUILD Started"
pip install -r requirements.txt

python3 manage.py collectstatic --no-input
python3 manage.py migrate
echo "Build Completed"