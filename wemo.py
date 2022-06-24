import pywemo
import configparser

configuration = configparser.ConfigParser()
configuration.read('config.ini')

WeMoName= configuration['WEMO'].get('switch_name')


WeMoFan = None


def getWeMo():
    #if WeMoFan == None:
    devices = pywemo.discover_devices() ## <-exception crashes.
    WeMoFan = next((x for x in devices if x.name == WeMoName), None)
    return WeMoFan
