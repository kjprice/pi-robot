cat /etc/os-release
cat /sys/firmware/devicetree/base/model
cat /proc/cpuinfo
uname -m
uname -a
sudo dpkg --print-architecture
arch
sudo file -Lb /usr/bin/ld | cut -d, -f2
hostnamectl
dpkg --print-foreign-architectures

# Get cortex
cat /sys/firmware/devicetree/base/cpus/cpu@1/compatible


### Package info

apt-cache search mongodb