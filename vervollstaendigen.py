import folium
import data_types as dt
from collect_data import AllStations, TrainConnection, TrainStation

stations = AllStations()
stations.load()

# def find_connection(in_, find_):
#     for connection in in_.connections:
#         if connection.station == find_:
#             return connection
#     return None


# for station in stations.stations.values():
#     if len(station.connections) == 0:
#         continue
#     for connection in station.connections:
#         connection.distance = round(connection.distance, 0)
#         other_ = find_connection(connection.station, station)
#         if other_ is None:
#             connection.station.add_connection(TrainConnection(station, connection.duration, connection.distance))
#         elif connection.duration < other_.duration:
#             if other_.distance != connection.distance:
#                 print(f"Distance mismatch: {other_.distance} vs. {connection.distance}")
#             other_.duration = connection.duration
#             other_.distance = connection.distance
            
#         else:
#             continue

# copy data to new object

network = dt.TrainNetwork()
for station in stations.stations.values():
    s = dt.Station(station.id, station.name, station.lat, station.lon, network)
    for connection in list(station.connections):
        c = {
                "id": station.id, 
                "name": station.name,
                "duration": connection.duration, 
                "location": {"latitude": station.lat, "longitude": station.lon}
               }
        s.add_connection(c)
    network.stations.add_station(s)

network.stations.get_station_by_id("8098262").find_lines()

network.lines.plot()
network.stations.plot()

    
# save D-Objects
network.save(filename="stations_D_voll.pickle")



# stations.save(filename="stations_voll.pickle")

# # export stations to json
# import json
# import os

# if not os.path.exists("data"):
#     os.makedirs("data")

# # with open("data/stations.json", "w") as f:
# #     json.dump(stations.stations, f, indent=4)

# # export stations to csv
# import csv

# with open("data/stations.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow(["id", "name", "lat", "lon"])
#     for station in stations.stations.values():
#         writer.writerow([station.id, station.name, station.lat, station.lon])

# # export connections to csv
# with open("data/connections.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow(["station_id", "connection_id", "duration", "distance"])
#     for station in stations.stations.values():
#         for connection in station.connections:
#             writer.writerow([station.id, connection.station.id, connection.duration, connection.distance])
