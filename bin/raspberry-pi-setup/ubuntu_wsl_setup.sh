# Things needed for a fresh ubuntu wsl on Windows
sudo apt update
sudo apt -y full-upgrade
sudo apt-get update

echo 'PATH=$PATH:~/.local/bin/' >> ~/.bash_profile

source ~/.bash_profile

sudo apt install python3-pip
sudo apt install -y python3-flask
sudo apt-get install -y jq

python3 -m pip install opencv-python
python3 -m pip install --no-input pynput
python3 -m pip install --no-input imagezmq
python3 -m pip install --no-input python-socketio
python3 -m pip install --no-input pandas
python3 -m pip install --no-input flask
python3 -m pip install --no-input flask-cors
python3 -m pip install --no-input eventlet