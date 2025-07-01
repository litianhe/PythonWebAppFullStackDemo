#!/bin/bash

# Load .env file from project root
set -a
[ -f ../.env ] && source ../.env
set +a


ENVIRONMENT=${ENVIRONMENT:-"production"}
python3 -m app.main