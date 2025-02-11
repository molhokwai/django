#!/usr/bin/env bash
# -*- coding: utf8 -*-
cd "/home/nkensa/GDrive-local/Tree/Workspaces/dev/frameworks/django/projects/django"
source venv/bin/activate
python manage.py check_tasks
notify-send "Webscraping" "Check tasks done..."