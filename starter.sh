#!/bin/bash
# make directory 
sudo mkdir -p "/var/html/www/rabiie/static/" 
sudo chmod -R 777 "/var/html/www/rabiie/static/"
sudo mkdir -p "/var/log/rabiie" 
sudo touch  "/var/log/rabiie/access.log"  
echo "static directory created"

sudo mkdir -p "/var/html/www/rabiie/media/"
sudo chmod -R 777 "/var/html/www/rabiie/media/"
echo "media directory created"

sudo mkdir -p "/var/html/www/rabiie/template/"
sudo chmod -R 777 "/var/html/www/rabiie/template/"

echo "template directory created"

# create database
sudo chmod +X create_db.sh
sh ./create_db.sh
cd  /home/ubuntu/iot/backend

# deploy database
sudo  cp ./rabiie.config  /etc/nginx/sites-available/rabiie
sudo ln -sf /etc/nginx/sites-available/rabiie /etc/nginx/sites-enabled/rabiie
sudo  cp ./rabiie.service  /etc/systemd/system/rabiie.service
echo "template directory created"
sudo  cp ./rabiie.socket  /etc/systemd/system/rabiie.socket
echo "template directory created"
sudo systemctl daemon-reload

python -m pip install pip

pip install -q -r req.txt

sudo nginx -t

sudo systemctl restart nginx

echo "sudo systemctl restart"
sudo systemctl restart rabiie.socket
sudo systemctl restart rabiie.service

sudo systemctl enable  rabiie.socket
sudo systemctl restart rabiie.service

black .

python manage.py makemigrations --settings core.settings.prod
python manage.py migrate --settings core.settings.prod
python manage.py collectstatic --no-input --settings core.settings.prod

sudo certbot --nginx -d bahateam.ir -d www.bahateam.ir
sudo systemctl restart nginx
echo "done"
