#!/usr/bin/env bash
# exit on error
# set -o errexit
ECHO "BUILD STARTED"
pip install -r requirements.txt
python3.9 manage.py collectstatic
ECHO "BUILD COMPLETED"