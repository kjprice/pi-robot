# Servo Motor

To get the servo Motor up and running, it is recommended to wire the servo up to the following pins (based on board numbers):
 - Red: 4 (Power)
 - Black: 6 (Ground)
 - White: 7 (IO)

From the raspberry pi, you can run `servo-simple.py` which will test out if it is all connecteed correctly

TODO:
 - Create python module (servo-module) to control servo
 - Create python module (read-faces) that can read an image and detect where a face is in the image
 - Create root python script that will:
  - pull a picture from the camera
  - Find where the nearest face is
  - Turn the servo in the direction of the face