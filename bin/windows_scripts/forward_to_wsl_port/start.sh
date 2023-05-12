#!/usr/bin/bash
cd "$(dirname "$0")"

source ./wsl_parameters.sh

function run_on_port() {
    PORT=$1
    # https://stackoverflow.com/questions/61002681/connecting-to-wsl2-server-via-local-network
    cmd1="netsh advfirewall firewall add rule name='Allowing LAN connections' dir=in action=allow protocol=TCP localport=$PORT"
    # cmd1="netsh advfirewall firewall add rule name="Allowing LAN connections" dir=in action=allow protocol=TCP localport=3000"

    cmd2="netsh interface portproxy add v4tov4 listenport=$PORT listenaddress=$WINDOWS_IP connectport=$PORT connectaddress=$WSL_IP"
    echo "Forwarding IP to WSL using the commands:"
    echo $cmd1
    echo $cmd2
    echo
    echo `$cmd1`
    echo `$cmd2`
    echo 
}

for port in ${PORTS[@]}; do
    run_on_port $port
done