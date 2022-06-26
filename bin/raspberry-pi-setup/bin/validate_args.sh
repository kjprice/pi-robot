hostname=$1

help_message=`cat text/help_message.txt`

if [ -z "$hostname" ] || [ "$hostname" = "--help" ]; then
    echo "$help_message"
    exit 1
fi