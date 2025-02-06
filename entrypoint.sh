#!/bin/sh
echo "172.17.0.1 mysql" >> /etc/hosts
cd /usr/src/environments/easyimovel
make prod
