. ../env/bin/activate
cd ../app/
pip install -r requirements/production.txt  | grep -v 'Requirement already satisfied' | grep -v 'Cleaning up...'
./manage.py collectstatic --noinput
./manage.py migrate -v 0
sudo /usr/local/bin/supervisorctl restart awecounting
