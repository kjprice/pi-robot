#!/bin/bash
cd "$(dirname "$0")"
cd ..

# Set environment variable for debugging mode
IS_TEST=true
export IS_TEST

help_message=`cat text/help_message.txt`
copy_ssh_key_message=`cat text/ssh-copy-id-text.txt`
send_setup_files_message=`cat text/ssh-scp-setup-files.txt`
run_setup_files_message=`cat text/ssh-run-setup-files.txt`

username='pi'

function assert_equals()
{
    cmd=$1
    expected_output="$2"
    output=`eval "$cmd"`
    if [ "$output" != "$expected_output" ]; then
        # error=<<-END
        # error=$''
        echo "Error"
        echo "Command: $cmd"
        echo "'$output' does not equal '$expected_output'."
        exit 1
    fi
}

test_hostname="test_hostname"

assert_equals './run.sh' "${help_message}"
assert_equals './run.sh --help' "${help_message}"

assert_equals './bin/validate_args.sh --help' "${help_message}"
assert_equals "./bin/validate_args.sh $test_hostname" ""

assert_equals './bin/get_config.sh username' $username
assert_equals './bin/get_config.sh setup_filepath' '/tmp/setup/'

IS_TEST=false assert_equals "./bin/run_command.sh 'echo yo'" "yo"
IS_TEST=true assert_equals "./bin/run_command.sh 'echo yo'" ""

expected_ssh_copy_key_command="ssh-copy-id $username@$test_hostname"
assert_equals "./bin/commands/ssh-copy-id.sh $test_hostname" "$expected_ssh_copy_key_command"

assert_equals "./bin/copy_ssh_key.sh $test_hostname" "$copy_ssh_key_message"

expected_scp_command="scp test/test1/* $username@$test_hostname:/tmp/test1/"
assert_equals "./bin/commands/scp.sh $test_hostname test/test1 /tmp/test1/" "$expected_scp_command"

assert_equals "./bin/send_setup_files.sh $test_hostname" "$send_setup_files_message"

expected_ssh_run_command="ssh $username@$test_hostname 'echo yo'"
assert_equals "./bin/commands/ssh-run.sh $test_hostname 'echo yo'" "$expected_ssh_run_command"

assert_equals "./bin/run_setup_files.sh $test_hostname" "$run_setup_files_message"