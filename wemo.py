import pywemo
import configparser

configuration = configparser.ConfigParser()
configuration.read('config.ini')

WeMoName= configuration['WEMO'].get('switch_name')


WeMoFan = None


def getWeMo():
    #if WeMoFan == None:
    devices = None
    try:
        devices = pywemo.discover_devices() ## <-exception crashes.
    except:
        return None
    WeMoFan = next((x for x in devices if x.name == WeMoName), None)
    return WeMoFan
