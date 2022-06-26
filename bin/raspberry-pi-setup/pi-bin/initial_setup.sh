cd "$(dirname "$0")"

sh step1_upgrade.sh

# Create Projects Folder
mkdir -p ~/Projects/pirobot

sh step2_install_depencies.sh

echo 
echo 'Setup is complete!!'