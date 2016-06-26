#!/bin/bash
project=awecounting
today=$(date +%F)
# set -x #echo on
echo "Dumping database on server..."
ssh ac "pg_dump awecounting > $today.sql"
echo "Fetching database dump..."
scp ac:~/$today.sql /tmp/$project-$today.sql
chmod 777 /tmp/$project-$today.sql
echo "Creating database and importing the dump..."
sudo su postgres sh -c "cd; createdb $project-$today; psql -X -1 -v ON_ERROR_STOP=1 -d $project-$today -f /tmp/$project-$today.sql > /dev/null"
echo "Update your settings to point to the database '$project-$today'"
if command -v xclip >/dev/null 2>&1; then
    echo $project-$today | tr -d '\r' | tr -d '\n' | xclip -sel clip
    echo "Copied database name to clipboard."
fi
echo "Finished!"
