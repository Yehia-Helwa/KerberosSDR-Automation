# KerberosSDR-Automation
Automates configuration and syncing of KerberosSDR

Python script is an older version using Selenium but was unable to run a headless browser leading to the development of the node js version.

Node js version uses Chrome API Puppetteer and is much faster than Selenium version while being more refined (automatically gets IP adress of pi). Looking into having it import the settings from settings.json and using those values for setup. Currently it requires you to open up the code and adjust the values based on your setup.

YOU WILL NEED TO INSTALL NODE JS ON YOUR PI FOR THIS TO WORK - Check out https://github.com/nebrius/raspi-io/wiki/Getting-a-Raspberry-Pi-ready-for-NodeBots#installing-nodejs

Since the Raspberry Pi uses chromium and not chrome you will also need to install the chromium webdriver. Check out https://www.youtube.com/watch?v=6LnJ1zW5464 if running into issues

INSTALLING CHROMIUM WEBDRIVER

sudo apt install chromium-browser chromium-codecs-ffmpeg

sudo install npm

npm install puppeteer-core@v1.11.0


