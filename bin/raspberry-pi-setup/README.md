# raspberry-pi-setup

Note that this was picked from https://gitlab.com/kjprice/raspberry-pi-setup

This is created to automate the setup for new raspberry pis. Additional documentation found in [GDrive](https://docs.google.com/document/d/168k9cZHiBqk0BG0d4QonVxRpl0W5Qmgc7nsR6axgqV0/edit#heading=h.su9eaeccbri)

To develop, run:

```
./bin/develop.sh
```

To run the entire script, run:
```
./run.sh {hostname} # {hostname} is the hostname of the raspberry pi to setup
```

To just send public keys to the raspberry pi, run:
```
./bin/copy_ssh_key.sh $hostname
```