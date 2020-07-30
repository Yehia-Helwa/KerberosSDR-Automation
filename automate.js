let puppeteer = require('puppeteer');



(async () => {
  var os = require('os');
  var ifaces = os.networkInterfaces();
  var addy
  Object.keys(ifaces).forEach(function (ifname) {
    var alias = 0;

    ifaces[ifname].forEach(function (iface) {
      if ('IPv4' !== iface.family || iface.internal !== false) {
        // skip over internal (i.e. 127.0.0.1) and non-ipv4 addresses
        return;
      }

      if (alias >= 1) {
        // this single interface has multiple ipv4 addresses
        console.log(ifname + ':' + alias, iface.address);
      } else {
        // this interface has only one ipv4 adress
      
	addy=iface.address
      }
      ++alias;
    });
  });


  console.log('IP address: '+addy)
  var http = 'http://'
  var goto  
  let browser = await puppeteer.launch({executablePath: '/usr/bin/chromium-browser'});
  let page = await browser.newPage();
  await page.goto(http.concat(addy,':8080/init'));
  await page.waitForSelector('.btn');
//CHANGE THESE VARS
  let centerFreq = '549';
  let sampFreq = '2';//The number refers to the index of the dropdown starting at 0, ex. '2' refers to the third choice from dropdown
  let gain = '15';//Use same index principle
  let filtBW = '200';
  let firTap = '100';
  let decimation = '1';
  let ant = '1';//Also index
//This is automatic calculating for the spacing using 0.333 spacing factor
  let calc = (299792458/(Number(centerFreq)*(10**6)))/3;
  let rcalc= calc.toFixed(4);
  let spacing = rcalc.toString();//if you want to use fixed value just add it here ex '0.14'(unit is meters)
  console.log('Spacing is '+spacing+' meters');
  let tDelay = 100 ;

  let centerFreqElem = await page.$('[name="center_freq"]');
  let sampFreqElem = 'select[name="samp_freq"]';
  let uniGainElem = await page.$('[name="uniform_gain"]');
  let gainElem = 'select[name="gain"]';
  let updateRecElem = await page.$('[value="Update Receiver Paramaters"]');

  
  

  await centerFreqElem.click({clickCount:3});
  await centerFreqElem.type(centerFreq);

  await page.select(sampFreqElem, sampFreq);

  if(!(await (await uniGainElem.getProperty('checked')).jsonValue())){
	await uniGainElem.click();  }

  await page.select(gainElem, gain);
   

//Updates receiver params
  await updateRecElem.click();
  console.log("Updated Receiver Paramaters")
  await page.waitFor(tDelay);  
  await page.goto(http.concat(addy,':8080/init'));
  await page.waitForSelector('.btn');

  let dcCompElem = await page.$('[name="dc_comp"]');
  let filtBWElem = await page.$('[name="filt_bw"]');
  let firTapElem = await page.$('[name="fir_size"]');
  let decimationElem = await page.$('[name="decimation"]');
  let updateIQElem = await page.$('[value="Update IQ Paramaters"]');

  
  if(!(await (await dcCompElem.getProperty('checked')).jsonValue())){
	await dcCompElem.click();  }
	
  await filtBWElem.click({clickCount:3});
  await filtBWElem.type(filtBW);
 
  await firTapElem.click({clickCount:3});
  await firTapElem.type('0');
 
  await decimationElem.click({clickCount:3});
  await decimationElem.type('1');
  await updateIQElem.click();
  console.log("Updated IQ with sync paramaters")
  await page.waitFor(tDelay);

  await page.goto(http.concat(addy,':8080/init'));
  await page.waitForSelector('.btn');
  let startProcessingElem = await page.$('[value="Start Processing"]');

  await startProcessingElem.click();
  await page.waitFor(tDelay);
  await page.goto(http.concat(addy,':8080/sync'));
  await page.waitForSelector('.btn');
  let enSyncElem = await page.$('[value="Enable Noise Source & Sync Display"]');
  let disableSyncElem = await page.$('[value="Disable Noise Source & Sync Display"]');

  try { await enSyncElem.click();}
  catch (error) { console.log("Noise source already enabled");}
  await page.waitFor(tDelay);
  await page.goto(http.concat(addy,':8080/sync'));
  await page.waitForSelector('.btn');
  let sampleSyncElem = await page.$('[value="Sample Sync"]');
  await page.waitFor(3000);
  await sampleSyncElem.click();	
  console.log("Beginning Sample Sync");
  await page.waitFor(tDelay);
  await page.goto(http.concat(addy,':8080/sync'));
  await page.waitFor(10000);
  let calibIQ = await page.$('[value="Calibrate IQ"]');
  await calibIQ.click();
  console.log("Beginning IQ Calibration");
  await page.waitFor(10000);
  
  await page.goto(http.concat(addy,':8080/sync'));
  await page.waitForSelector('.btn');
  enSyncElem = await page.$('[value="Enable Noise Source & Sync Display"]');
  disableSyncElem = await page.$('[value="Disable Noise Source & Sync Display"]');

  try { await disableSyncElem.click();}
  catch (error) { console.log("Noise source already off");}
  console.log("Syncing done, disabline noise source")
  await page.waitFor(tDelay); 
  await page.goto(http.concat(addy,':8080/init'));
  await page.waitForSelector('.btn');

  dcCompElem = await page.$('[name="dc_comp"]');
  filtBWElem = await page.$('[name="filt_bw"]');
  firTapElem = await page.$('[name="fir_size"]');
  decimationElem = await page.$('[name="decimation"]');
  updateIQElem = await page.$('[value="Update IQ Paramaters"]');

  
  if(!(await (await dcCompElem.getProperty('checked')).jsonValue())){
	await dcCompElem.click();  }
	
  await filtBWElem.click({clickCount:3});
  await filtBWElem.type(filtBW);
 
  await firTapElem.click({clickCount:3});
  await firTapElem.type(firTap);
 
  await decimationElem.click({clickCount:3});
  await decimationElem.type(decimation);
  await updateIQElem.click();
  console.log("Updated IQ with actual paramaters")
  await page.waitFor(tDelay);

  
  await page.goto(http.concat(addy,':8080/doa'));
  await page.waitForSelector('.btn');
  let antElem = 'select[name="ant_arrangement"]';
  let spacingElem = await page.$('[name="ant_spacing"]');
  let enDOAElem = await page.$('[name="en_doa"]');
  let enBartElem = await page.$('[name="en_bartlett"]');
  let enCaponElem = await page.$('[name="en_capon"]');
  let enMEMElem = await page.$('[name="en_MEM"]');
  let enMUSICElem = await page.$('[name="en_MUSIC"]');
  let updateDOAElem = await page.$('[value="Update DOA"]');

  await page.select(antElem, ant);
  await spacingElem.click({clickCount:3});
  await spacingElem.type(spacing);
  if(!(await (await enDOAElem.getProperty('checked')).jsonValue())){
	await enDOAElem.click();  }
  if((await (await enBartElem.getProperty('checked')).jsonValue())){
	await enBartElem.click();  }
  if((await (await enCaponElem.getProperty('checked')).jsonValue())){
	await enCaponElem.click();  }
  if((await (await enMEMElem.getProperty('checked')).jsonValue())){
	await enMEMElem.click();  }
  if(!(await (await enMUSICElem.getProperty('checked')).jsonValue())){
	await enMUSICElem.click();  }
  await updateDOAElem.click();
  console.log("Updated DOA parameters");
  await page.waitFor(tDelay);
  console.log("Closing browser");
//  await page.screenshot({path: 'screenshot.png'});
  await browser.close();
})();
