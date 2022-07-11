# Setup Raspberry Pi
All package depencies and initial setup for a raspberry pi can be found in `./bin/raspberry-pi-setup/pi-bin/initial_setup.sh`.

To configure a raspberry pi, you can use the utility `./bin/raspberry-pi-setup/run.sh`, which will run [initial_setup.sh](/bin/raspberry-pi-setup/pi-bin/initial_setup.sh).

To configure a new host that can control the raspberry pis (like a ubuntu server or mac), run [ubuntu_wsl_setup.sh](/bin/raspberry-pi-setup/ubuntu_wsl_setup.sh). See specific information for WSL setup below.


# Startup scripts

Running the utility to setup a raspberry pi (see above) will also create a script to be run every time the raspberry pi boots up. The script (found [here](/bin/raspberry-pi-setup/pi-bin/init.d/robot_startup.sh) locally) is copied to the raspberry pi's /etc/init.d folder.

### Startup script

All raspbberry pis will then run the same command:
```
/home/pi/Projects/pirobot/bin/on_pi_startup/run_for_hostname.sh || true &
```

The [run_for_hostname.sh](/bin/on_pi_startup/run_for_hostname.sh) script will see if there is a startup file that matches the hostname of the machine. For example, the hostname `pi3misc2` will run /bin/on_pi_startup/startup_by_hostname/pi3misc2.sh.

# Servo Motor

To get the servo Motor up and running, it is recommended to wire the servo up to the following pins (based on board numbers):
 - Red: 4 (Power)
 - Black: 6 (Ground)
 - White: 7 (IO)

From the raspberry pi, you can run `servo-simple.py` which will test out if it is all connecteed correctly

The servo accepts a "duty" (a number between 2-12) which determines where to turn. The duty will have to turn 2.9 duties to span a single entire image from the camera (as of this commit).

# Web App
Front end code can be found at /web-app/
Back end code can be found at /python/web_app/

### Build files
The web files are built using react. To build all files, run:

```
cd web-app
npm install
npm run build
```

These build files can now be found in /web-app/build/

### Develop React
In addition to building files which will be saved, you can start a react dev server that will rebuild all files when any file is saved during developed. This can be done by running:

```
cd web-app
npm install
npm start
```

# Server Running On WSL
WSL makes it easy to run a linux server on Windows. The drawback is that http traffic to the WSL server is blocked outside windows. To get around this, we can use port forwarding.

After running the web_app server (`./bin/run/run_web_server.sh`) within wsl, we can run a script on windows to start port forwarding. 

### Start Forwarding
On Windows run:

```
./bin/windows_scripts/forward_to_wsl_port/start.sh
```

### End Forwarding
On Windows run:

```
./bin/windows_scripts/forward_to_wsl_port/end.sh
```

### Print Services Running On Port
To check if windows is listening on a port, run the following (replace `PORT` with desired port such as `9898`):
```
netstat -ano | findstr :PORT
```

### Resources
This solution helped me tremendously:
 -  https://stackoverflow.com/questions/11525703/port-forwarding-in-windows

# TODO:
 - [ ] Add symbolic links on raspberry pis to all shell scripts they might need (add to ~/bin/ and set PATH)
 - [ ] Add symbolic links on raspberry pis to all logs (`~/Projects/pirobot/data/logs` -> `/var/logs/`)
 - [ ] Log *everything* that runs on the raspberry pis
 - [ ] Move log path directories to config.json
 - [ ] Add UI to web-app to display all logs
 - [ ] Add UI to web-app to display videos from security - stream from shell?
 - [ ] Display all error logs unique from regular logs
 - [ ] Make sure that the security camera is taking clear videos
 - [ ] Upload security camera videos to the cloud
 - [ ] Why are startup logs empty? http://pi3misc2:8001/logs/startup/
 - [ ] Process status should change in real time (eg, clicking on "start process" does not immediately react)
 - [ ] Add button to reboot raspberry pis
 - [ ] Fix "recent logs" to work with new log directory
 
 
 
 
 
 
 
 