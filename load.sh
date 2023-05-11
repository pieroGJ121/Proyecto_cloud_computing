#!/usr/bin/env sh

psql -U postgres -d project_dbp -a -f sql/script.sql
psql -U postgres -d project_dbp -a -f sql/script2.sql
psql -U postgres -d project_dbp -a -f sql/script3.sql
psql -U postgres -d project_dbp -a -f sql/script4.sql

python app.py

psql -d project_dbp -a -f sql/script.sql
psql -d project_dbp -a -f sql/script2.sql
psql -d project_dbp -a -f sql/script3.sql
psql -d project_dbp -a -f sql/script4.sql
