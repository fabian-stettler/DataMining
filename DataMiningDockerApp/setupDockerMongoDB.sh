#!/bin/bash


# Update and install necessary packages
apt-get update && apt-get install -y wget gnupg && \
    wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add - && \
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list && \
    apt-get update && apt-get install -y mongodb-database-tools cron

# Start MongoDB
mongod --bind_ip_all --fork --logpath /var/log/mongodb.log

# Wait for MongoDB to start
sleep 5

# Run the init script
/docker-entrypoint-initdb.d/init-mongo.sh

# Setup cron job
echo "0 22 * * * root mongodump --out /backup/dump-\$(date +\%F) --uri='mongodb://admin:secret@localhost:27017/?authSource=admin' && mongoexport --uri='mongodb://admin:secret@localhost:27017/Datamining_Srf?authSource=admin' --collection=Articles --out=/backup/currentData.json --jsonArray >> /var/log/cron.log 2>&1" > /etc/cron.d/mongobackup

# Apply the cron job
crontab /etc/cron.d/mongobackup

# Start cron service
cron

# Keep the container running
tail -f /dev/null
