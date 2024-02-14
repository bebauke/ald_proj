# generate a adjacency matrix from the data. The positions of the stations within the matrix is taken from the file station_coords.csv.

import pandas as pd
import numpy as np
import folium
import geopy.distance as gd

# add file directory to path
# import sys
# sys.path.append("data")


df_stations = pd.read_csv("data/station_coords.csv")
df_connections = pd.read_csv("data/train_data.csv")

# init new column "connections" in df_stations
df_stations["connections"] = None

for con in df_connections.iterrows():
    # find station in df_stations and add train to new column "connections" in df_stations
    field = df_stations[df_stations["station"] == con[1]["station"]] 
    if len(field) == 0: # station not found...
        # continue
        raise "Station not found in df_stations" 

    field = field.index[0]
    if df_stations.at[field, "connections"] is None:
        df_stations.at[field, "connections"] = [con[1]["train"]]
    else:
        df_stations.at[field, "connections"].append(con[1]["train"])


df_stations

# add another column with connections as list of dicts with keys "id", "duration" 
lines = df_connections.groupby("train")

import networks as nw

g = nw.Graph(list(df_stations["station"]))

for line in lines:
    for i in range(len(line[1]["station"])-1):
        # get duration from current station to next station (departure - arrival at next station)
        depart = line[1]["departure"].iloc[i]
        arrive = line[1]["arrival"].iloc[i+1]

        # to time format
        depart = pd.to_datetime(depart, format="%H:%M")
        arrive = pd.to_datetime(arrive, format="%H:%M")
        # calculate duration in minutes (int)
        duration = int((arrive - depart).seconds / 60)
        # add edge to graph
        g.update_edge(line[1]["station"].iloc[i], line[1]["station"].iloc[i+1], duration)

print(g.get_neighbors("Wien Hbf"))

print(pd.DataFrame(g.adjacency_matrix).to_csv("data/adjacency_matrix.csv", index=False))

# create a map with all stations and connections

# create map
m = folium.Map(location=[48.2082, 16.3738], zoom_start=10)

# add markers for stations
for s in df_stations.iterrows():
    # folium.Marker([s[1]["lat"], s[1]["lon"]], popup=s[1]["station"]).add_to(m)
    folium.Circle([s[1]["lat"], s[1]["lon"]], radius=100, popup=s[1]["station"], color="red", fill=True, fill_color="red").add_to(m)

# add connections from adjacency matrix
for i in range(len(g.adjacency_matrix)):
    for j in range(len(g.adjacency_matrix)):
        if g.adjacency_matrix[i][j] != np.inf:
            distance = gd.distance((df_stations["lat"][i], df_stations["lon"][i]), (df_stations["lat"][j], df_stations["lon"][j])).km
            popup = str(g.adjacency_matrix[i][j]) + " min, " + str(round(distance, 2)) + " km"
            folium.PolyLine([[df_stations["lat"][i], df_stations["lon"][i]], [df_stations["lat"][j], df_stations["lon"][j]]],popup=popup, color="black", weight=4*distance/g.adjacency_matrix[i][j], opacity=1).add_to(m)

# save map
m.save("data/map.html")
# g.to_csv("adjacency_matrix.csv")

