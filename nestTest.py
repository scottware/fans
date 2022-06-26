import nest
import configparser

# configuration = configparser.ConfigParser()
# configuration.read('config.ini')
#
# client_id = configuration['NEST'].get('client_id')
# client_secret = configuration['NEST'].get('client_secret')
# nest_auth_url = configuration['NEST'].get('nest_auth_url')
# access_token_cache_file = configuration['NEST'].get('access_token_cache_file')
# product_version = configuration['NEST'].getint('product_version')
# nest_name = configuration['NEST'].get('thermostat_name')


class NestTest:
    Thermostat = None

    def __init__(self, thermostat_name, client_id, client_secret, access_token_cache_file):
        self.thermostatName = thermostat_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token_cache_file = access_token_cache_file

    def getThermostat(self, thermostatName):
        napi = nest.Nest(client_id=self.client_id, client_secret=self.client_secret,
                         access_token_cache_file=self.access_token_cache_file)


        thermostat = next((x for x in napi.thermostats if x.name == self.thermostatName), None)
        return thermostat

    def getNestTemp(self):
        if self.Thermostat == None:
            self.Thermostat = self.getThermostat(self.thermostatName)
            print("fetching thermostat ", self.thermostatName)
        return self.Thermostat.temperature


if __name__ == "__main__":
    import time

    client_id = '7a1e3c11-f705-45ca-b24b-1034f7f920c3'
    client_secret = '6dKJ8PEPxlpIQYqJyfnAbMiNm'
    nest_auth_url = 'https://home.nest.com/login/oauth2?client_id=7a1e3c11-f705-45ca-b24b-1034f7f920c3&state=STATE'
    access_token_cache_file = 'nest.json'
    product_version = 1337
    bedroom_thermostat_name = 'Bedroom'
    kitchen_thermostat_name = 'Kitchen'

    bed = NestTest(bedroom_thermostat_name, client_id, client_secret, access_token_cache_file)
    kit = NestTest(kitchen_thermostat_name, client_id, client_secret, access_token_cache_file)
    while True:
        bed_temp = bed.getNestTemp()
        kit_temp = kit.getNestTemp()

        print("{0} {1}".format(bed_temp, kit_temp))
        time.sleep(2)
