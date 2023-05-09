#!/usr/bin/env sh

python app.py

psql -d project_dbp -a -f script.sql
psql -d project_dbp -a -f script2.sql
psql -d project_dbp -a -f script3.sql
psql -d project_dbp -a -f script4.sql
