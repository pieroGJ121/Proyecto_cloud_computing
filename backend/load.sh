#!/usr/bin/env sh

psql -d project_dbp -a -f "sql/script_uuid.sql"

python app.py

for file in script.sql script2.sql script3.sql script4.sql
do
    psql -d project_dbp -a -f "sql/$file"
done
