echo "  # Installing Common Utilities for WSL and Raspberry PI # "

python3 -m pip install --upgrade pip


# Networking/Connectivity
python3 -m pip install --no-input imagezmq
python3 -m pip install --no-input python-socketio
python3 -m pip install --no-input "python-socketio[client]"
sudo apt install -y python3-flask
python3 -m pip install --no-input flask
python3 -m pip install --no-input flask-cors

# Install common ML libraries
python3 -m pip install pandas
python3 -m pip install opencv-python
python3 -m pip pip install -U scikit-learn # sklearn

# Concurrency
python3 -m pip install --no-input eventlet


# Read JSON in shell commands
sudo apt-get install -y jq


## Mongo
python3 -m pip install --no-input pymongo

# Keyboard/mouse events
python3 -m pip install --no-input pynput

# NVM and Node.js
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
nvm install stable
source  ~/.bashrc
npm install -g nodemon
