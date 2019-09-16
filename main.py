import requests


class UsefulData:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def extract_bus_number_with_times(self):
        bus_arrival_dict = {}
        departures_response = self.raw_data["departures"]
        for bus_num in departures_response:
            departures_for_bus = []
            for bus in departures_response[bus_num]:
                departures_for_bus.append(bus["best_departure_estimate"])
            bus_arrival_dict[bus_num] = departures_for_bus
        print(bus_arrival_dict)
        return bus_arrival_dict

    def print_bus_times(self, buses):
        for bus in buses:
            print("Bus number " + bus + " is estimated to arrive at: " + str(buses[bus]))


class WebData:
    def __init__(self):
        self.atcocode = '0180BAC30592'
        self.url = 'https://transportapi.com/v3/uk/bus/stop/' + self.atcocode + \
                   '/live.json?app_id=3f307260&app_key=1f62a399e530d84bb9c271fd491343d4&group=' \
                   'route&limit=5&nextbuses=yes'

    def read_url(self):
        r = requests.get(self.url)
        return r.json()


def main():
    print("Welcome to BusBoard.")
    website = WebData()
    web_data = website.read_url()
    useful_data = UsefulData(web_data)
    print(web_data)
    buses = useful_data.extract_bus_number_with_times()
    useful_data.print_bus_times(buses)

if __name__ == "__main__":
    main()
