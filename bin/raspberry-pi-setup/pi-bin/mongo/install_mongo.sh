#!/bin/bash
cd "$(dirname "$0")"

# ./install_mongo_from_source.sh
./install_mongo_from_s3.sh
./install_mongo_tools.sh

./setup_mongo.sh



# TODO: Try to strip https://www.mongodb.com/community/forums/t/add-mongodb-4-2-arm64-builds-for-raspberry-pi-os-64-bit-debian-buster/5046

# for x in mongo*; do strip -s $x; file $x; du -sh $x; done 

# TODO: Run:
# use admin
# db.createUser( { user: "admin",
#             pwd: "SUPERSECRETPASSWORD",
#             roles: [ "userAdminAnyDatabase",
#                      "dbAdminAnyDatabase",
#                      "readWriteAnyDatabase"] } )
