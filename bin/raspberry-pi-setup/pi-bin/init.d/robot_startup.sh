#!/bin/bash
# Taken from https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#init

# /etc/init.d/robot_startup
### BEGIN INIT INFO
# Provides:          robot_startup
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

runuser -l pi -c '/home/pi/Projects/pirobot/bin/on_pi_startup/run_for_hostname.sh || true &'
