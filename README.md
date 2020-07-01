# KerberosSDR-Automation
Automates configuration and syncing of KerberosSDR


[b]To use it you need to install some dependencies:[/b]
sudo pip3 install selenium
sudo apt-get install chromium-chromedriver

[b]To run:[/b] [i](check below before running)[/i]
Download file to Pi through whatever means you want, VNC etc.
Open up terminal and cd to wherever the script is located
Run it using - [i]python3 automate.py[/i]

[b]Before you run it make sure:[/b]
You open up the script and change the variables at the top to whatever settings you want inputted
Nothing or 50 ohm terminals are connected to antenna inputs
Raspberry Pi has had enough time to start the kerberos software
Best to run from clean boot or after rebooting software
