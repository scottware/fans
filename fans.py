import wemo
import nestTest
import weather
import time
import datetime
# import database
import configparser
import math
import json

# targetTemp = 67.0
# updateRate = 290  # seconds

configuration = configparser.ConfigParser()
configuration.read('config.ini')
client_id = configuration['NEST'].get('client_id')
client_secret = configuration['NEST'].get('client_secret')
# nest_auth_url = configuration['NEST'].get('nest_auth_url')
access_token_cache_file = configuration['NEST'].get('access_token_cache_file')
# product_version = configuration['NEST'].getint('product_version')
bedroom_thermostat_name = configuration['NEST'].get('bedroom_thermostat_name')
kitchen_thermostat_name = configuration['NEST'].get('kitchen_thermostat_name')

bedroomNest = nestTest.NestTest(bedroom_thermostat_name, client_id, client_secret, access_token_cache_file)
kitchenNest = nestTest.NestTest(kitchen_thermostat_name, client_id, client_secret, access_token_cache_file)

print ("{0}: {1:4} {2:3} {3:4} {4}".format("Time", "outsideTemp", "insideTemp", "targetTemp",
                                    "wemoSwitch"))

while True:

    targetTemp = configuration['APP'].getfloat('target_temp')
    updateRate = configuration['APP'].getint('update_frequency')
    now = datetime.datetime.now()
    desiredState = 0

    wemoSwitch = wemo.getWeMo()
    if wemoSwitch == None:
        print("failed to find wemo")
        time.sleep(10)
        continue

    outsideTemp = weather.wunderGroundTemp()
    if (outsideTemp == None):
        print("failed to get temp")
        time.sleep(10)
        continue

    try:
        bedroomTemp = bedroomNest.getNestTemp()
        kitchenTemp = kitchenNest.getNestTemp()
    except:
        print("failed to connect to nest:")
        # print(nt.NestBedroom)
        bedroomNest.NestBedroom = None
        kitchenNest.NestKitchen = None
        time.sleep(10)
        continue

    if configuration['APP'].get('status') == 'off':
        if wemoSwitch.get_state() != 0:
            wemoSwitch.set_state(0)
        print(
            "{0}: {1:4} {2:3} {3:4} {4} -- System is OFF".format(now.strftime("%c"), outsideTemp, insideTemp, targetTemp,
                                                wemoSwitch.get_state()))
        # database.insert(outsideTemp, insideTemp, targetTemp, desiredState)
        sleepTime = updateRate - math.floor(time.time()) % updateRate
        time.sleep(sleepTime)
        continue

    insideTemp = (bedroomTemp + kitchenTemp) / 2.0
    if (insideTemp <= targetTemp):
        desiredState = 0
    else:
        delta = insideTemp - float(outsideTemp)
        if (6 <= now.hour <= 9):
            # print('morning shuts off 2° early')
            delta -= 2
        if delta > 0:
            desiredState = 1
        else:
            desiredState = 0

    if wemoSwitch.get_state() != desiredState:
        wemoSwitch.set_state(desiredState)
        print("--- State Change at {0} ---".format(now.strftime("%c")))

    print(
        "{0}: {1:4} {2:3} {3:4} {4}".format(now.strftime("%c"), outsideTemp, insideTemp, targetTemp,
                                            wemoSwitch.get_state()))

    #store for webview
    webstate = {}
    webstate['time'] = now.strftime("%b %d, %I:%M %p")
    webstate['outsideTemp'] = outsideTemp
    webstate['kitchenTemp'] = kitchenTemp
    webstate['bedroomTemp'] = bedroomTemp
    webstate['targetTemp'] = targetTemp
    webstate['desiredState'] = 'green' if desiredState == 1 else 'red'
    file = open("webstate.json", "w")
    file.write(json.dumps(webstate))
    file.close()

    # database.insert(outsideTemp, insideTemp, targetTemp, desiredState)
    sleepTime = updateRate - math.floor(time.time()) % updateRate
    if updateRate != 290:
        print("next update in {0} seconds".format(sleepTime))
    time.sleep(sleepTime)
