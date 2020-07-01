#Script that automates the setup for kerberossdr, change variable values at top of code to what inputs you will use.
#Plug in your terminals before starting script and switch them out with your antennas after it runs.
#Author: Yehia Helwa
#Created: 7/1/2020

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time

#input variables here
#make sure that all your inputs are valid entries on the webpage otherwise you will get an error thrown back, values listed below confirmed to work
centerFreq='433.3'
sampFreq='1.024'
gain='28.0'
filtBW='10'
firTap='100'
decimation='1'
antArrang='UCA'
spacing='0.24' #spacing in meters




#selecting chromium browser
waitDelay=10
options= Options()
browser=webdriver.Chrome(options=options, executable_path='/usr/bin/chromedriver')
type(browser)

#go to config page
browser.get('http://192.168.0.120:8080/init')


centerFreqElem= WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "center_freq")))
centerFreqElem.clear()
centerFreqElem.send_keys(centerFreq)
print("Inputted center frequency with value <%s>" %centerFreq)

sampFreqElem= WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "samp_freq")))
select = Select(sampFreqElem)
select.select_by_visible_text(sampFreq)
print("Inputted sample frequency with value <%s>" %sampFreq)

uniGainElem = WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.ID, "uniform_gain_id")))
if not uniGainElem.is_selected():
 uniGainElem.click()
print("Enabled uniform gain")

gainElem= WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "gain")))
select = Select(gainElem)
select.select_by_visible_text(gain)
print("Selected gain with value <%s>" %gain)


#update receiver params
updateReciever = WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/form/div[9]/input')))
updateReciever.click()
print("Updated receiver parameters")
time.sleep(2)

dcCompElem =  WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "dc_comp")))
if not dcCompElem.is_selected():
 dcCompElem.click()
print("Enabled DC compensation")

filtBwElem=WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div[3]/div[2]/input')))
filtBwElem.clear()
filtBwElem.send_keys(filtBW)

firTapElem= WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "fir_size")))
firTapElem.clear()
firTapElem.send_keys('0')

decimationElem= WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "decimation")))
decimationElem.clear()
decimationElem.send_keys('1')
print("Set syncing IQ parameters")


#update IQ params
updateIQ = WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div[6]/input')))
updateIQ.click()
print("Updated IQ parameters")
time.sleep(2)

#start processing
startProc=WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/form[1]/div/input')))
startProc.click()
print("Started processsing")
time.sleep(2)

#start spectrum display
# browser.find_element_by_xpath('/html/body/div[5]/form[1]/div/input').click()	
# time.sleep(0.5)

#switch to sync
browser.get('http://192.168.0.120:8080/sync')
print("Switching to sync tab")


#enable noise source and sync display
syncButton=WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/form[1]/div/input')))
syncButtonTxt=syncButton.get_attribute("value")
if(syncButtonTxt=="Enable Noise Source & Sync Display"):
 print("NS and SD disabled now enabling")
 syncButton.click()
elif(syncButtonTxt=="Disable Noise Source & Sync Display"):
 print("NS and SD enabled (not supposed to happen)")
time.sleep(4)

#sample sync then calibrate calibrate iq
sampleSync=WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form[2]/div/input')))
sampleSync.click()	
print("Syncing system ...")
time.sleep(6)


calibIQ=WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form[3]/div/input')))
calibIQ.click()	
print("Calibrating IQ ...")
time.sleep(6)

#disable noise source and sync display
syncButtonTxt=browser.find_element_by_xpath("/html/body/div[2]/form[1]/div/input").get_attribute("value")
if(syncButtonTxt=="Enable Noise Source & Sync Display"):
 print("NS and SD disabled (not supposed to happen)")
elif(syncButtonTxt=="Disable Noise Source & Sync Display"):
 print("NS and SD enabled now disabling (syncing done)")
 browser.find_element_by_xpath("/html/body/div[2]/form[1]/div/input").click()
time.sleep(3)

#switch back config to update FIR tap and decimation
browser.get('http://192.168.0.120:8080/init')
print("Switching to config tab to update IQ parameters")


dcCompElem = WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "dc_comp")))
if not dcCompElem.is_selected():
 dcCompElem.click()

filtBwElem=WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div[3]/div[2]/input')))
filtBwElem.clear()
filtBwElem.send_keys(filtBW)

firTapElem= WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "fir_size")))
firTapElem.clear()
firTapElem.send_keys(firTap)

decimationElem= WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "decimation")))
decimationElem.clear()
decimationElem.send_keys(decimation)
print("Inputted actual IQ parameters")


#update IQ params

updateIQ = WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div[6]/input')))
updateIQ.click()
print("Updated IQ parameters")
time.sleep(2)


#switch to doa
browser.get('http://192.168.0.120:8080/doa')
print("Switching to DOA tab")


#select UCA arrangement
antArrangElement= WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "ant_arrangement")))
select = Select(antArrangElement)
select.select_by_visible_text(antArrang)
print("Selected <%s> arrangement" %antArrang)


#set spacing
antSpacing= WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "ant_spacing")))
antSpacing.clear()
antSpacing.send_keys(spacing)
print("Setting spacing of <%s> meters" %spacing)


#enable DOA
enDOA = WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "en_doa")))
if not enDOA.is_selected():
 enDOA.click()

#disable all algorithims except MUSIC
enBartlett=WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "en_bartlett")))
enCapon=WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "en_capon")))
enMEM=WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "en_MEM")))
enMUSIC=WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.NAME, "en_MUSIC")))
if enBartlett.is_selected():
	enBartlett.click()

if enCapon.is_selected():
	enCapon.click()

if enMEM.is_selected():
	enMEM.click()

if not enMUSIC.is_selected():
	enMUSIC.click()

print("Enabling DOA and disabling all algorithims except MUSIC")
time.sleep(2)

updateDOA=WebDriverWait(browser, waitDelay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/div[6]/input')))
updateDOA.click()
print("DOA enabled!")
time.sleep(5)
print("Shutting down browser")
browser.quit()

