# Servo Motor

To get the servo Motor up and running, it is recommended to wire the servo up to the following pins (based on board numbers):
 - Red: 4 (Power)
 - Black: 6 (Ground)
 - White: 7 (IO)

From the raspberry pi, you can run `servo-simple.py` which will test out if it is all connecteed correctly

The servo accepts a "duty" (a number between 2-12) which determines where to turn. The duty will have to turn 2.9 duties to span a single entire image from the camera (as of this commit).

# Web App
Front end code can be found at /web-app/
Back end code can be found at python/web_app.py

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

# Startup scripts

We are currently adding a script to etc/rc.local to run at startup. Note that eventually we want to create an init.d file once our [Raspberry-pi-setup](https://gitlab.com/kjprice/raspberry-pi-setup) repo is merged into this repo.

To "automatically" update the rc.local file to all servers, run:

```
.bin/run/run_set_startup_scripts.sh
```

> Note that you still need to manually edit the `/etc/rc.local` file and move the `exit 0` line to the end of the file. Obviously this is not ideal.

### Startup script

All raspbberry pis will then run the same command:
```
/home/pi/Projects/pirobot/bin/on_pi_startup/run_for_hostname.sh || true &
```

The [run_for_hostname.sh](/bin/on_pi_startup/run_for_hostname.sh) script will see if there is a startup file that matches the hostname of the machine. For example, the hostname `pi3misc2` will run /bin/on_pi_startup/startup_by_hostname/pi3misc2.sh.

# TODO:
 - [ ] Combine `set_startup_script.sh` with /bin/raspberry-pi-setup/run.sh
 - [ ] Add symbolic links on raspberry pis to all shell scripts they might need (add to ~/bin/ and set PATH)
 - [ ] Add symbolic links on raspberry pis to all logs (`~/Projects/pirobot/data/logs` -> `/var/logs/`)
 - [ ] Log *everything* that runs on the raspberry pis
 - [ ] Move log path directories to config.json
 - [ ] Add endpoint to server_status to retrieve most recent log (`./bin/logs/read_last_log.sh`)
 
 