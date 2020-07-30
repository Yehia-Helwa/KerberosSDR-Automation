#!/bin/bash

BUFF_SIZE=256 #Must be a power of 2. Normal values are 128, 256. 512 is possible on a fast PC.
#IPADDR="0.0.0.0"
IPPORT="8081"

# set to /dev/null for no logging, set to some file for logfile. You can also set it to the same file. 
RTLDAQLOG="rtl_daq.log"
SYNCLOG="sync.log"
GATELOG="gate.log"
PYTHONLOG="python.log"

#RTLDAQLOG="/dev/null"
#SYNCLOG="/dev/null"
#GATELOG="/dev/null"
#PYTHONLOG="/dev/null"

# If you want to kill all matching processes on startup without prompt. Otherwise, set it to anything else. 
FORCE_KILL="yes"


### Uncomment the following section to automatically get the IP address from interface wlan0 ###
### Don't forget to comment out "IPADDR="0.0.0.0" ###

IPADDR=$(ip addr show wlan0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1)
while [ "$IPADDR" == "" ] || [ "$IPADDR" == "169.254.*" ]
do
sleep 1
echo "waiting for network"
IPADDR=$(ip addr show wlan0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1)
echo $IPADDR
done

### End of Section ###

# Useful to set this on low power ARM devices
sudo cpufreq-set -g performance

# Set for RPI3 with heatsink/fan
#sudo cpufreq-set -d 1.4GHz
# Set for Tinkerboard with heatsink/fan
#sudo cpufreq-set -d 1.8GHz


# Trap SIGINT (2) (ctrl-C) as well as SIGTERM (6), run cleanup if either is caught
trap cleanup 2 6

cleanup() {
	# Kill all processes that have been spawned by this program.
	# we know that these processes have "_receiver", "_GUI" and "_webDisplay" in their names. 
	exec 2> /dev/null           # Suppress "Terminated" message. 
	sudo pkill -f "_receiver" 
	sudo pkill -f "_GUI"
	sudo pkill -f "_webDisplay" 
	
	# also delete all pipes: 
	rm -f _receiver/C/gate_control_fifo
        rm -f _receiver/C/sync_control_fifo
        rm -f _receiver/C/rec_control_fifo
}


# Clear memory
sudo sh -c "echo 0 > /sys/module/usbcore/parameters/usbfs_memory_mb"
echo '3' | sudo dd of=/proc/sys/vm/drop_caches status=none

echo "Starting KerberosSDR"

sudo kill $(ps aux | grep 'rtl' | awk '{print $2}')
sudo pkill rtl_daq
sudo pkill sim
sudo pkill sync
sudo pkill gate
sudo pkill python3

# Enable on the Pi 3 to prevent the internet from hogging the USB bandwidth
sudo wondershaper wlan0 3000 3000
sudo wondershaper eth0 3000 3000

sleep 1

# Create RAMDISK for jpg files
sudo mount -osize=30m tmpfs /ram -t tmpfs

# Remake Controller FIFOs. Deleting them should not be neccessary after 
# a clean exit, but why not do it anyway... 
rm -f _receiver/C/gate_control_fifo
mkfifo _receiver/C/gate_control_fifo

rm -f _receiver/C/sync_control_fifo
mkfifo _receiver/C/sync_control_fifo

rm -f _receiver/C/rec_control_fifo
mkfifo _receiver/C/rec_control_fifo

# Start programs at realtime priority levels
curr_user=$(whoami)

sudo chrt -r 50 taskset -c 3 ionice -c 1 -n 0 ./_receiver/C/rtl_daq $BUFF_SIZE 2>$RTLDAQLOG 1| \
	sudo chrt -r 50 taskset -c 3 ./_receiver/C/sync $BUFF_SIZE 2>$SYNCLOG 1| \
	sudo chrt -r 50 taskset -c 3 ./_receiver/C/gate $BUFF_SIZE 2>$GATELOG 1| \
	sudo nice -n -20 sudo -u $curr_user python3 -O _GUI/hydra_main_window.py $BUFF_SIZE $IPADDR &>$PYTHONLOG &
#automate
sleep 20
node automate.js
# Start PHP webserver which serves the updating images
echo "Python Server running at $IPADDR:8080"
echo "PHP Server running at $IPADDR:$IPPORT"
sudo php -S $IPADDR:$IPPORT -t _webDisplay >&- 2>&-
