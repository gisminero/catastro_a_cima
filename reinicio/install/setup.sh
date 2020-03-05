#!/bin/bash
sudo cp reinicio.service /etc/systemd/system -y
sudo chmod 777 /etc/systemd/system/reinicio.service -y
sudo chmod +x /etc/systemd/system/reinicio.service -y
sudo cd /opt/api3 -y
sudo chmod -R 777 reinicio -y
sudo cd reinicio -y
sudo chmod +x start.sh -y
sudo chmod +x main.py -y
