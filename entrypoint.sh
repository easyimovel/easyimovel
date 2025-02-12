#!/bin/sh
echo "172.17.0.1 mysql" >> /etc/hosts
crond
cd /usr/src/environments/easyimovel
fastapi run
