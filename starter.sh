#!/bin/bash

sudo cp ./rabiie.config  /etc/nginx/sites-available/rabiie
sudo cp ./rabiie.config  /etc/nginx/sites-enabled/rabiie
sudo cp ./rabiie.service  /etc/systemd/system/rabiie.service
sudo cp ./rabiie.socket  /etc/systemd/system/rabiie.socket
echo done
