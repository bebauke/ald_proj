import os
import pickle
import matplotlib.pyplot as plt
import app.helpers.train_guru_api as tgapi
from math import radians, sin, cos, sqrt, atan2
import numpy as np
from tqdm import tqdm
import folium

api = tgapi.StationAPI(base_url="https://api.direkt.bahn.guru")
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## There is a need for knowing the directions of the connections (inherents from TrainStation)

class TrainNetwork:
    def __init__(self):
        self.stations = Stations(self)
        self.lines = Lines(self)

    def save(self, filename="network.pickle"):
        try:
            with open(filename, "wb") as file:
                pickle.dump(self, file)
            return True
        except Exception as e:
            print(f"Error saving stations: {e}")
            return False

    def load(self, filename="network.pickle"):
        if os.path.exists(filename):
            try:
                with open(filename, "rb") as file:
                    loaded_stations = pickle.load(file)
                self.stations = loaded_stations.stations
                return True
            except Exception as e:
                print(f"Error loading stations: {e}")
        return False
    
class Lines:
    line_id = 1

    def __init__(self, network=None):
        self.network = network
        self.lines = {}

    def add_line(self, line):
        if line.id == None:
            line.id = Lines.line_id
            Lines.line_id += 1
        if line.id not in self.lines:
            self.lines[line.id] = line
            return True
        else:
            return False

    def get_line_by_id(self, line_id):
        return self.lines.get(line_id, None)
    
    def plot(self):
        map = folium.Map(location=[50.110924, 8.682127], zoom_start=6)
        for line in self.lines.values():
            # draw lines between the stations
            _last_station = None
            for station in line.stations:
                if _last_station is not None:
                    folium.PolyLine([[_last_station.lat, _last_station.lon], [station.lat, station.lon]], color="red", weight=2.5, opacity=1).add_to(map)
                _last_station = station
        map.save("map_lines.html")

class Stations:
    def __init__(self, network=None):
        self.network = network
        self.stations = {}

    def add_station(self, station):
        from archiv.collect_data import TrainStation 
        if type(station) == Station:
            if station.id not in self.stations:
                self.stations[station.id] = station
                return True
            else:
                return False
        elif type(station) == TrainStation:
            if station.id not in self.stations:
                self.stations[station.id] = Station(station.id, station.name, station.lat, station.lon, self.network)
                for connection in station.connections:
                    self.stations[station.id].add_connection()
                return True
            else:
                return False

    def get_station_by_id(self, station_id):
        return self.stations.get(station_id, None)
    
    def find_station(self, station_name):
        for station in self.stations.values():
            if station.name == station_name:
                return station
        return None
    
    def plot(self):
        map = folium.Map(location=[50.110924, 8.682127], zoom_start=6)
        for station in self.stations.values():
            folium.Marker([station.lat, station.lon], popup=f"{station.name}, {station.id}").add_to(map)
        map.save("map_stations.html")
    

class Line:
    def __init__(self, connections1, connections2):
        # connections is a List, for each station two connections.
        # we want a ordered list of the stations and the duration and distance between them.
        # A error should be thrown if the durtion or distance are miss matched between the entries.
        self.stations = []
        self.id = None

        def neg_direction(numbers):
            # Sort the list of numbers
            sorted_numbers = sorted(numbers)

            # Calculate the midpoint
            midpoint = len(sorted_numbers) // 2

            # Split the list into two groups
            group1 = sorted_numbers[:midpoint]
            group2 = sorted_numbers[midpoint:]

            # Calculate the median for each group using numpy
            median1 = np.median(group1)
            median2 = np.median(group2)

            return (median1 + median2 + np.pi) / 2
        
        con_dir = [d.direction for d in connections1] + [d.direction for d in connections2]
        neg = neg_direction(con_dir)

        # if the direction is within +- pi/2 of neg_direction, invert the duration and distance

        _stations1 = [(c.station.id, c.direction, c.distance, c.duration) for c in connections1]
        _stations2 = [(c.station.id, c.direction, c.distance, c.duration) for c in connections2]

        for i, station in enumerate(_stations1):
            if station[1] < neg + np.pi/2 and station[1] > neg - np.pi/2:
                _stations1[i] = (station[0], station[1], -station[2], -station[3])

        for i, station in enumerate(_stations2):
            if station[1] < neg + np.pi/2 and station[1] > neg - np.pi/2:
                _stations2[i] = (station[0], station[1], -station[2], -station[3])

        _stations1.sort(key=lambda x: x[2])
        _stations2.sort(key=lambda x: x[2])

        # subtract the duration and distance of the first station from all stations
        _stations1 = [(s[0], s[1], s[2]-_stations1[0][2], s[3]-_stations1[0][3]) for s in _stations1]
        _stations2 = [(s[0], s[1], s[2]-_stations2[0][2], s[3]-_stations2[0][3]) for s in _stations2]

        # compare the lists and raise an error if the stations are not the same
        print(_stations1)
        print(_stations2)

class Connection:
    id_counter = 1

    def __init__(self, station, duration, distance, direction):
        self.id = Connection.id_counter
        self.station = station
        self.duration = duration
        self.distance = distance
        self.direction = direction
        Connection.id_counter += 1

    def __str__(self):
        return f"TrainConnection({self.station}, {self.duration}, {self.distance})"

# class to store the stations
class Station:
    def __init__(self, id, name, lat, lon, network):
        self.network = network
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.connections = set() 
        self.conD = set() # only for next stations in a line (fastest on a line)
        self.lines = set()
        network.stations.add_station(self)

    @classmethod
    def from_id(cls, id): # class method to create a station from an id
        station = None
        try:
            station = api.get_station_by_id(id)
        except:
            print("Error while getting station")
        name = station["name"]
        lat = station["location"]["latitude"]
        lon = station["location"]["longitude"]
        return cls(id, name, lat, lon)
        
    def update_connections(self):
        connections = []
        if len(self.connections) > 0: # if the connections are already loaded, don't load them again
            return
        try:
            connections = api.get_reachable_from(self.id)
        except:
            print("Error while getting connections")
        for connection in connections:
            self.add_connection(connection)
    
    def add_connection(self, connection):
        def distance(self, lon, lat):
            coord1 = {'latitude': self.lat, 'longitude': self.lon}
            coord2 = {'latitude': lat, 'longitude': lon}
            
            R = 6371.0 # Radius of the Earth in kilometers
            
            # Convert latitude and longitude from degrees to radians
            lat1, lon1 = radians(coord1['latitude']), radians(coord1['longitude'])
            lat2, lon2 = radians(coord2['latitude']), radians(coord2['longitude'])

            # Calculate the differences between latitudes and longitudes
            dlat = lat2 - lat1
            dlon = lon2 - lon1

            # Haversine formula
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            # Distance in kilometers
            distance_km = R * c

            # Return distance in kilometers and duration in hours
            return round(distance_km)
        
        def direction(self, lon, lat):
            coord1 = {'latitude': self.lat, 'longitude': self.lon}
            coord2 = {'latitude': lat, 'longitude': lon}
            
            # Convert latitude and longitude from degrees to radians
            lat1, lon1 = radians(coord1['latitude']), radians(coord1['longitude'])
            lat2, lon2 = radians(coord2['latitude']), radians(coord2['longitude'])
            
            # Calculate the differences between latitudes and longitudes
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            # Calculate the direction
            direction = atan2(dlon, dlat)
            
            # Return direction in radians
            return direction

        if type(connection) == dict:
            obj = Station(connection["id"], connection["name"], connection["location"]["latitude"], connection["location"]["longitude"], self.network)
            self.connections.update({Connection(obj, 
                connection['duration'],
                distance(self, connection["location"]["longitude"], connection["location"]["latitude"]),
                direction(self, connection["location"]["longitude"], connection["location"]["latitude"])
                )})
        elif type(connection) == Connection:
            self.connections.update(connection)

    def find_next_stations(self, nearest = 5, speediest = 25):
        _list = []
        if len(self.connections) == 0:
            self.update_connections()
        for connection in self.connections:
            _list.append((connection.station, connection.duration, connection.distance))
        con_first = _list[:nearest]
        _list.sort(key=lambda x: x[1]/x[2] if x[2] != 0 else 0)
        _list = con_first+_list[:speediest]

        tqdm_ = tqdm(_list, desc=f"Updating connections for {self.name}")
        for connection in tqdm_:
            tqdm_.set_description(f"Updating connections for {self.name} - {connection[0].name}")
            connection[0].update_connections()

        return set([connection[0] for connection in _list])
    
    def find_lines(self):
        # if the station is in connections, find common connections and add them to a line

        # go thru all connections. if there is a connection to a station without a line, add it to a new line
        # if the line is a subset of another line, remove the line and add the stations to the other line.
        # the duration must be equal to the subsets duration.
        def common_line(self, station):
            for line in self.lines:
                if station in line.stations:
                    return line
            return None
        
        stations = self.find_next_stations()
        print (f"Found {len(stations)} stations")

        # stations in self.connections and in station.connections
        for station in stations:
            if len(station.connections) == 0:
                station.update_connections()
            selfStations = set([con.station for con in self.connections]+[self])
            stationStations = set([con.station for con in station.connections]+[station])

            common = selfStations.intersection(stationStations)

            from_self = [con for con in self.connections if con.station in common] + [Connection(self,0,0,1)]
            from_station = [con for con in station.connections if con.station in common] + [Connection(station,0,0,1)]

            if len(common) > 0:
                line = Line(from_self, from_station)
                self.network.lines.add_line(line)
                for station in line.stations:
                    station.lines.add(line)


        # for station in stations:
        #     if len(station

        # for con in self.connections:
        #     # if stations have a common line already, skip
        #     if common_line(self, con.station) is not None:
        #         continue

        #     overlap1 = set() # set([Connection(self,0,0,1)])
        #     overlap2 = set() # set([Connection(con.station,0,0,1)])

        #     for con_b in con.station.connections:
        #         if con_b.station == con.station:
        #             overlap1.update({con})
        #             overlap2.update({con_b})

        #     line = Line(overlap1, overlap2)

        #     self.network.lines.add_line(line)
        #     for station in line.stations:
        #         station.lines.add(line)
