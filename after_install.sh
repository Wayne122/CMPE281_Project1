cd /home/ubuntu/django/project1
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate

sudo service apache2 restart