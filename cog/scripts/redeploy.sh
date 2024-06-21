#!/bin/bash
source .env
echo 'Loaded Environment:'  $NODE_ENV
echo 'Cloning Repo:'  $REPO


sudo rm -rf mars5-tts
git clone $REPO
sudo groupadd docker
sudo chmod 666 /var/run/docker.sock
sudo systemctl start docker
docker system prune --all --force
bash mars5-tts/cog/scripts/deploy.sh