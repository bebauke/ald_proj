# %%
# in file train_data.csv - get a set of all stations and get coordinates for each station from google maps
import pandas as pd
import geopy

df = pd.read_csv("train_data.csv")
# stations as set
stat = set(df["station"])
df = pd.DataFrame(columns=["station", "lat", "lon"])
not_found = []

geolocator = geopy.Nominatim(user_agent="find_coords_for_stations")

for s in stat:
    # get coordinates for each station
    location = geolocator.geocode(s + " Bhf")
    if location is None:
        not_found.append(s)
        print(s)
        continue
    print(s, location.latitude, location.longitude)
    df = pd.concat([df, pd.DataFrame([[s, location.latitude, location.longitude]], columns=["station", "lat", "lon"])])
# get coordinates for each station
df

# %%

not_found

# %%

s = [ 'Wien Leopoldau Bahnhst',
      'Himberg b.Wien',
      'Gaisruck b.Stockerau', 
      'Hausleiten b.Stockerau', 
      'Wien Stadlau Bahnhst', 
      'Wien Spittelau Bahnhst', 
      'Wien Mitte-Landstraße Bf',
      'Wien Quartier Belvedere Bahnhst', 
      'Wien Ottakring Bahnhst', 
      'Wien St.Marx Bahnhst',
      'Wien Aspern Nord Bf',
      'Wien Handelskai Bahnhst']
k = ['48.27840481938549, 16.45380639493707',
     '48.08250138244009, 16.44535412942819',
     '48.39424846635467, 16.064578900600033',
     '48.39148244722903, 16.106262088273617',
     '48.21936450517845, 16.448405008551163',
     '48.23564316585537, 16.3582739071101',
     '48.20616968626435, 16.38488801692848', 
     '48.18820976212593, 16.381815737807862',  
     '48.21194943578536, 16.310980018272126',
     '48.18807476066042, 16.39977066904048',
     '48.234914559741895, 16.504452894516263',
     '48.242538643147824, 16.385825011657854'  
     ]

df_ = pd.DataFrame(columns=["station", "lat", "lon"])
for i in range(len(s)):
    df_ = pd.concat([df_, pd.DataFrame([[s[i], k[i].split(",")[0], k[i].split(",")[1]]], columns=["station", "lat", "lon"])])

df = pd.concat([df, df_])

df.to_csv("station_coords.csv", index=False)


# %%
import pandas as pd
df = pd.read_csv("station_coords.csv")
# if there are index columns - remove / reset index
df = df.drop(columns=["Unnamed: 0"])
df.to_csv("station_coords.csv", index=True)

# %%
