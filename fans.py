import wemo
import nestTest
import weather
import time
import datetime
# import database
import configparser
import math
import json

wemoSwitch = None

configuration = configparser.ConfigParser()
configuration.read('config.ini')
client_id = configuration['NEST'].get('client_id')
client_secret = configuration['NEST'].get('client_secret')
access_token_cache_file = configuration['NEST'].get('access_token_cache_file')
bedroom_thermostat_name = configuration['NEST'].get('bedroom_thermostat_name')
kitchen_thermostat_name = configuration['NEST'].get('kitchen_thermostat_name')

bedroomNest = nestTest.NestTest(bedroom_thermostat_name, client_id, client_secret, access_token_cache_file)
kitchenNest = nestTest.NestTest(kitchen_thermostat_name, client_id, client_secret, access_token_cache_file)

print ("{0}: {1:4} {2:3} {3:4} {4}".format("Time", "outsideTemp", "insideTemp", "targetTemp",
                                    "wemoSwitch"))

while True:
    ## Needs to be reopened so that changes are picked up
    configuration = configparser.ConfigParser()
    configuration.read('config.ini')

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
        bedroomNest.NestBedroom = None
        kitchenNest.NestKitchen = None
        time.sleep(10)
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

    if configuration['APP'].get('status') == 'off':
        if wemoSwitch.get_state() != 0:
            wemoSwitch.set_state(0)

    elif wemoSwitch.get_state() != desiredState:
        wemoSwitch.set_state(desiredState)
        print("--- State Change at {0} ---".format(now.strftime("%b %d, %I:%M %p")))

    print(
        "{0}: {1:4}º {2:3}º {3:4}º Setting:{4} System:{5}".format(now.strftime("%b %d, %I:%M %p"),
               outsideTemp, insideTemp, targetTemp,
                'ON' if wemoSwitch.get_state() == 1 else 'OFF',
               configuration['APP'].get('status').upper() ))

    sleepTime = updateRate - math.floor(time.time()) % updateRate
    time.sleep(sleepTime)
