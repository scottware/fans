import wemo
import nestTest
import weather
import time
import datetime
import database

targetTemp = 67.0
updateRate = 290  # seconds

nt = nestTest.NestTest()

while True:
    now = datetime.datetime.now()

    outsideTemp = weather.wunderGroundTemp()
    if (outsideTemp == None):
        print("failed to get temp")
        time.sleep(5)
        continue

    try:
        insideTemp = nt.getNestTemp()
    except:
        print("failed to connect to nest:")
        print(nt.NestBedroom)
        nt.NestBedroom = None
        time.sleep(10)
        continue

    wemoSwitch = wemo.getWeMo()
    if wemoSwitch == None:
        print("failed to find wemo")
        time.sleep(10)
        continue

    if (insideTemp <= targetTemp):
        desiredState = 0
    else:
        delta = insideTemp - float(outsideTemp)
        if (5 <= now.hour <= 10):
            print('morning shuts off 1° early')
            delta-=1
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
    time.sleep(updateRate)
