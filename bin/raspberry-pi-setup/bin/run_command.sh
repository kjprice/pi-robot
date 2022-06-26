# Runs a command if not a test

command="${@: -1}" # Last arg


if [ "$IS_TEST" != true ] ; then
    eval "$command"
fi