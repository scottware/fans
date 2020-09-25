import wemo
import nestTest
import weather
import time
import datetime
import database
import configparser

# targetTemp = 67.0
# updateRate = 290  # seconds

nt = nestTest.NestTest()
print ("{0}: {1:4} {2:3} {3:4} {4}".format("Time", "outsideTemp", "insideTemp", "targetTemp",
                                    "wemoSwitch"))

while True:

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
        insideTemp = nt.getNestTemp()
    except:
        print("failed to connect to nest:")
        # print(nt.NestBedroom)
        nt.NestBedroom = None
        time.sleep(10)
        continue

    if configuration['APP'].get('status') == 'off':
        if wemoSwitch.get_state() != 0:
            wemoSwitch.set_state(0)
        print(
            "{0}: {1:4} {2:3} {3:4} {4} -- System is OFF".format(now.strftime("%c"), outsideTemp, insideTemp, targetTemp,
                                                wemoSwitch.get_state()))
        database.insert(outsideTemp, insideTemp, targetTemp, desiredState)
        time.sleep(updateRate)
        continue

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
    database.insert(outsideTemp, insideTemp, targetTemp, desiredState)
    if updateRate != 290:
        print("next update in {0} seconds".format(updateRate))
    time.sleep(updateRate)
