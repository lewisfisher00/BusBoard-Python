import requests


class BusTimesData:
    def __init__(self, atcocode):
        self.atcocode = atcocode
        self.bus_times_url = f'https://transportapi.com/v3/uk/bus/stop/{self.atcocode}/live.json?app_id=3f307260&' \
                             'app_key=1f62a399e530d84bb9c271fd491343d4&group=route&limit=5&nextbuses=no'

    def read_bus_times_url(self):
        r = requests.get(self.bus_times_url)
        return r.json()


class BusStopsData:
    def __init__(self, lat_lon):
        self.lat_lon = lat_lon

    def get_atcocodes(self):
        bus_stops_info = requests.get("https://transportapi.com/v3/uk/places.json?"
                                      "app_id=3f307260&app_key=1f62a399e530d84bb9c271fd491343d4&"
                                      f"lat={self.lat_lon[0]}&lon={self.lat_lon[1]}&type=bus_stop").json()
        stops = []
        find = bus_stops_info["member"]
        for stop in range(0, 2):
            stops.append(find[stop]["atcocode"])
        return stops


class PostcodeTravelInfo:
    def __init__(self, postcode, stops):
        self.postcode = postcode
        self.lat = str(self.obtain_lat())
        self.lon = str(self.obtain_lon())
        self.stops = stops

    def get_post_info(self):
        return requests.get(f'http://api.postcodes.io/postcodes/{self.postcode}').json()

    def obtain_lat(self):
        post_ifo = self.get_post_info()
        try:
            lat = str(post_ifo["result"]["latitude"])
        except:
            lat = 0
        return lat

    def obtain_lon(self):
        post_ifo = self.get_post_info()
        try:
            lon = str(post_ifo["result"]["longitude"])
        except:
            lon = 0
        return lon

    def __str__(self):
        output = f'Postcode entered: {self.postcode}'
        for stop in self.stops:
            output += str(stop)
        return output


class Stop:
    def __init__(self, name, departures):
        self.name = name
        self.departures = departures

    def __str__(self):
        output = f'\n\t- Stop name: {self.name}'
        for departure in self.departures:
            output += str(departure)
        return output


class Departure:
    def __init__(self, time, bus_num):
        self.time = time
        self.bus_num = bus_num

    def __str__(self):
        return f'\n\t\t -Bus {self.bus_num} will arrive at {self.time}.'


def create_full_data_struct(postcode):
    full_details_for_postcode = PostcodeTravelInfo(postcode, [])
    if (full_details_for_postcode.lat == 0) & (full_details_for_postcode.lon == 0):
        return 0
    else:
        atcocodes = BusStopsData((full_details_for_postcode.lat, full_details_for_postcode.lon)).get_atcocodes()
        for atcocode in atcocodes:
            raw_stop = BusTimesData(atcocode).read_bus_times_url()
            stop = Stop(raw_stop["name"], [])
            raw_departures = raw_stop["departures"]
            for bus_num in raw_departures:
                raw_departures_for_number = raw_departures[bus_num]
                for raw_depart in raw_departures_for_number:
                    dep = Departure(
                        raw_depart["best_departure_estimate"],
                        raw_depart["line_name"])
                    stop.departures.append(dep)
            full_details_for_postcode.stops.append(stop)
    return full_details_for_postcode


def main_cmd():
    print("Welcome to BusBoard.")
    valid = False
    while not valid:
        post_code = input("Enter your postcode: ")
        result = create_full_data_struct(post_code)
        if result == 0:
            print("Invalid postcode, try again.")
        else:
            valid = True
            print(result)


# main_cmd()
