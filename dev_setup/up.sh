#!/bin/bash

# Get the script directory
SCRIPTPATH="$(pwd)/dev_setup"

# Start the Docker Compose stack using the newer 'docker compose' command
docker compose -f "$SCRIPTPATH/docker-compose.yml" up --build

# # Wait for a few seconds to ensure containers are up
# sleep 3

# # SETUP DATABASE ROLES AND PERMISSIONS
# docker exec database-node sh -c "/cockroach/cockroach sql -u root --insecure --host=database-node < /docker-entrypoint-initdb.d/init.sql"
