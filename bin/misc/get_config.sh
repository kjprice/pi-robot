#!/bin/bash
cd "$(dirname "$0")"

cd ../..

field_name="$1"
config=`cat config.json`

field_value=`echo $config | jq ".$field_name"`
data_type=`echo $field_value | jq "type"`

if [ "$data_type" = '"array"' ]; then
  # Send output as raw (can be iterated on)
  echo $field_value | jq --raw-output '.[]'
else
  # Send output as raw string
  echo $field_value | jq --raw-output '.'
fi

