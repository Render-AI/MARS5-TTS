#!/bin/bash
source .env
echo 'Loaded Environment:'  $NODE_ENV
echo 'Cloning Repo:'  $REPO

# cog push
cd mars5-tts/cog
sudo groupadd docker
sudo chmod 666 /var/run/docker.sock
sudo systemctl start docker
cog push $REPLICATE_MODEL