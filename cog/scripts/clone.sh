#!/bin/bash
source .env
echo 'Loaded Environment:'  $NODE_ENV
echo 'Cloning Repo:'  $REPO

# git clone
git clone $REPO