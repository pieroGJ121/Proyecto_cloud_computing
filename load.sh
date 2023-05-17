#!/usr/bin/env sh

python app.py

for file in script.sql script2.sql script3.sql script4.sql
do
    psql -d project_dbp -a -f "sql/$file"
done
