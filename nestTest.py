import nest
import configparser

configuration = configparser.ConfigParser()
configuration.read('config.ini')

client_id = configuration['NEST'].get('client_id')
client_secret = configuration['NEST'].get('client_secret')
nest_auth_url = configuration['NEST'].get('nest_auth_url')
access_token_cache_file = configuration['NEST'].get('access_token_cache_file')
product_version = configuration['NEST'].getint('product_version')
nest_name = configuration['NEST'].get('themostat_name')


class NestTest:
    Thermostat = None

    def getThermostat(self, thermostatName):
        napi = nest.Nest(client_id=client_id, client_secret=client_secret,
                         access_token_cache_file=access_token_cache_file)
        thermostat = next((x for x in napi.thermostats if x.name == thermostatName), None)
        return thermostat

    def getNestTemp(self):
        if self.Thermostat == None:
            self.Thermostat = self.getThermostat(nest_name)
            print("fetching themostat")
        return self.Thermostat.temperature


if __name__ == "__main__":
    import time

    nt = NestTest()
    while True:
        temp = nt.getNestTemp()
        print(temp)
        time.sleep(2)
