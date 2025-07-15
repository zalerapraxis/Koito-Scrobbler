#!/usr/bin/env bash

# Check if the service process is running
if pgrep -f koito-scrobbler-service.py > /dev/null; then
  exit 0
fi

# Fallback to HTTP health endpoint
if curl --fail http://localhost:8000/health > /dev/null; then
  exit 0
fi

exit 1