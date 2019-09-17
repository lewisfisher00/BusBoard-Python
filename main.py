import requests


class postcode:
    def __init__(self, postcode_input):
        self.postcode_input = postcode_input
        self.latitude = str(self.obtain_lat())
        self.longitude = str(self.obtain_lon())

    def get_post_info(self):
        return requests.get('http://api.postcodes.io/postcodes/' + self.postcode_input).json()

    def obtain_lon(self):
        post_ifo = self.get_post_info()
        try:
            lon = str(post_ifo["result"]["longitude"])
        except:
            lon = 0
        return lon

    def obtain_lat(self):
        post_ifo = self.get_post_info()
        try:
            lat = str(post_ifo["result"]["latitude"])
        except:
            lat = 0
        return lat

    def get_closest_bus_stops(self):
        bus_stops_info = requests.get("https://transportapi.com/v3/uk/places.json?"
                                      "app_id=3f307260&app_key=1f62a399e530d84bb9c271fd491343d4&"
                                      "lat=" + self.latitude + "&lon=" + self.longitude + "&type=bus_stop").json()
        stops = {}
        find = bus_stops_info["member"]
        for stop in range(0, 2):
            atcocode = find[stop]["atcocode"]
            name = find[stop]["name"]
            stops[atcocode] = name
        return stops

    @staticmethod
    def display_error():
        print("Invalid postcode enter, try again.")


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
        return bus_arrival_dict

    @staticmethod
    def print_bus_times_main(buses, name):
        for bus in buses:
            print("Bus number " + bus + " is estimated to arrive at: " + str(buses[bus]) + " at the " + name + " stop.")


class raw_json_info:
    def __init__(self, atcocode):
        self.atcocode = atcocode
        self.url = 'https://transportapi.com/v3/uk/bus/stop/' + self.atcocode + \
                   '/live.json?app_id=3f307260&app_key=1f62a399e530d84bb9c271fd491343d4&group=' \
                   'route&limit=5&nextbuses=no'

    def read_url(self):
        r = requests.get(self.url)
        return r.json()


def cm_main():
    print("Welcome to BusBoard.")
    valid = False
    postcode_to_use = ''
    while not valid:
        post_code = input("Enter your postcode: ")
        postcode_to_use = postcode(post_code)
        if (postcode_to_use.latitude == '0') & (postcode_to_use.longitude == '0'):
            postcode_to_use.display_error()
        else:
            valid = True
    stops = postcode_to_use.get_closest_bus_stops()
    for stop in stops:
        website = raw_json_info(stop)
        useful_data = UsefulData(website.read_url())
        buses = useful_data.extract_bus_number_with_times()
        useful_data.print_bus_times_main(buses, stops[stop])


def webpage_main(post_code):
    postcode_to_use = postcode(post_code)
    if (postcode_to_use.latitude == '0') & (postcode_to_use.longitude == '0'):
        return 0
    stops = postcode_to_use.get_closest_bus_stops()
    output = []
    for stop in stops:
        website = raw_json_info(stop)
        useful_data = UsefulData(website.read_url())
        buses = useful_data.extract_bus_number_with_times()
        output.append((buses, stops[stop]))
    return output


if __name__ == "__main__":
    cm_main()
