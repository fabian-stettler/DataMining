#!/bin/bash
# Initialisieren der Datenbank und Laden der JSON-Datei
sleep 5

# Die Umgebungsvariablen MONGO_INITDB_ROOT_USERNAME und MONGO_INITDB_ROOT_PASSWORD werden verwendet
admin="admin"
secret="secret"

mongosh <<EOF
use admin
db.createUser({
  user: '$admin',
  pwd: '$secret',
  roles: [{ role: 'root', db: 'admin' }]
})
db.auth('$admin', '$secret')
use Datamining_Srf
db.Articles.drop()
db.createCollection('Articles')
EOF

# Laden der JSON-Datei in die Collection
mongoimport --db Datamining_Srf --collection Articles --file /docker-entrypoint-initdb.d/currentData.json --jsonArray

echo "DB is loaded correctly!"
echo "Initialisierung der DB fertig."