from lxml import html
import requests
import configparser
from pprint import pprint

configuration = configparser.ConfigParser()
configuration.read('config.ini')

pws_weather_station = configuration['WEATHER'].get('pws_weather_station')
pws_weather_station_backup = configuration['WEATHER'].get('pws_weather_station_backup')
wunderground_station = configuration['WEATHER'].get('wunderground_station')


def outsideTemp():
    page = requests.get(pws_weather_station_backup)
    page = requests.get(pws_weather_station)

    tree = html.fromstring(page.content)
    s = tree.find_class("stationobs-detail")
    tr = s[0].findall('tr')
    last = tr[2].find_class('u-eng')
    try:
        temp, unit = last[0].text.split('°')
        return temp
    except:
        print("failed to parse:")
        print(page.content)
        return None


def wunderGroundTemp():
    page = requests.get(wunderground_station)

    tree = html.fromstring(page.content)
    # try:
    #     s = tree.get_element_by_id("curTemp")
    # except:
    #     print("failed to parse:")
    #     print(page.content)
    #     return None
    # try:
    #     obj = s.find_class("wx-value")
    #     temp = obj[0].text
    # except:
    #     print("failed to parse (2):")
    #     print(page.content)
    #     temp = None
    try:
        s = tree.find_class("test-true wu-unit wu-unit-temperature is-degree-visible ng-star-inserted")
    except:
        print("failed to parse:")
        print(page.content)
        return None

    try:
        t = s[0].text_content()
        temp = t[0:-3]

    except:
        print("failed to parse (2):")
        print(page.content)
        temp = None

    return temp


if __name__ == "__main__":
    print("get temp: {0}".format(wunderGroundTemp()))
