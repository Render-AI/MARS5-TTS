#!/bin/bash
source .env
echo 'Loaded Environment:'  $NODE_ENV
echo 'Cloning Repo:'  $REPO

sudo rm -rf mars5-tts
git clone $REPO