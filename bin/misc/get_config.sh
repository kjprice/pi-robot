#!/bin/bash
cd "$(dirname "$0")"

cd ../..

field_name="${@: -1}"

cat config.json | jq .$field_name
