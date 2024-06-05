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

# Mongo
python3 -m pip install --no-input pymongo

# Keyboard/mouse events
python3 -m pip install --no-input pynput

# NVM and Node.js
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
nvm install stable
source  ~/.bashrc
npm install -g nodemon


##########################

#### Helpful commands ####
# Taken from https://www.infoworld.com/article/3715352/9-command-line-jewels-for-your-developer-toolkit.html

# bat (like `cat` but better) https://github.com/sharkdp/bat?tab=readme-ov-file#installation
sudo apt install bat
mkdir -p ~/.local/bin
ln -s /usr/bin/batcat ~/.local/bin/bat

# fzf (fuzzy finder) https://github.com/junegunn/fzf?tab=readme-ov-file#installation
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install

# Read JSON in shell commands
sudo apt-get install -y jq 

# tldr (like `man` but better)
npm install -g tldr

echo 'ngrok (awesome reverse proxy - make local servers public)'
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
  sudo gpg --dearmor -o /etc/apt/keyrings/ngrok.gpg && \
  echo "deb [signed-by=/etc/apt/keyrings/ngrok.gpg] https://ngrok-agent.s3.amazonaws.com buster main" | \
  sudo tee /etc/apt/sources.list.d/ngrok.list && \
  sudo apt update && sudo apt install ngrok
ngrok config add-authtoken 1Qxzg0ySLAvaZFh6GkMBldXWFgz_2TV8GeWMgvWwy6eAJ6Hyg # Super secret token

##########################
