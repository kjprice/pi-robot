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