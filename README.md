# KerberosSDR-Automation
Automates configuration and syncing of KerberosSDR

To use this you will need the automate.js file as well as to install the dependencies.

Node js version uses Chrome API Puppetteer and is much faster than Selenium version while being more refined (automatically gets IP adress of pi). Looking into having it import the settings from settings.json and using those values for setup. Currently it requires you to open up the code and adjust the values based on your setup.

YOU WILL NEED TO INSTALL NODE JS ON YOUR PI FOR THIS TO WORK - Check out https://github.com/nebrius/raspi-io/wiki/Getting-a-Raspberry-Pi-ready-for-NodeBots#installing-nodejs

Since the Raspberry Pi uses chromium and not chrome you will also need to install the chromium webdriver. Check out https://www.youtube.com/watch?v=6LnJ1zW5464 if running into issues


INSTALLING CHROMIUM WEBDRIVER

sudo apt install chromium-browser chromium-codecs-ffmpeg

sudo install npm

npm install puppeteer-core@v1.11.0


After this run the file using

node automate.js

I personally have incorporated the script into the run.sh file inside the kerberossdr folder and have included my own run.sh file in case anyone wants to use it. (make sure automate.js is in same folder of run.sh)


BEFORE RUNNING MAKE SURE:

You open up the script and change the variables at the top to whatever settings you want inputted

Nothing or 50 ohm terminals are connected to antenna inputs

Raspberry Pi has had enough time to start the kerberos software

Best to run from clean boot or after rebooting software
