import requests
from bs4 import BeautifulSoup
import pandas as pd

count = 0

def scrape_db_station_info(url, df = None):
    global count
    count = count + 1
    # static count for train
    # Sending a GET request to the webpage
    if df is None:
        df = pd.DataFrame(columns=["station", "link", "arrival", "departure", "platform", "train"])
    
    try:
        page = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return []

    # Parsing the HTML content
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Extracting relevant data
    # Assuming the data is in table format (adjust the code according to the actual HTML structure)
    # h1 contains information for Train
    train = soup.find("h1").text.strip("Fahrtinformationen zu ").replace(" ", "")+"_{:03d}".format(count)
    print("\n"+train)

    data = []
    table = soup.find(id="trainroute")
    if table is None:
        raise Exception("No table found")

    rows = table.find_all(class_="tqRow")
    if len(rows) == 0:
        raise Exception("No rows found")
    
    print(len(rows), end=" ")

    for row in rows:
        
        stat = row.find_all(class_="station")
        arrival = row.find_all(class_="arrival")
        departure = row.find_all(class_="departure")
        platform = row.find_all(class_="platform")

        # remove all tqContentHL spans
        if len(stat) == 0:
            # put caracter c to console
            print("c", end="")
            continue

        try:
            for s in stat:
                if s.span is not None:
                    s.span.decompose()
            for a in arrival:
                if a.span is not None:
                    a.span.decompose()
            for d in departure:
                if d.span is not None:
                    d.span.decompose()
            for p in platform:
                if p.span is not None:
                    p.span.decompose()
        except AttributeError as e:
            # put caracter a to console
            print("e", end="")
            continue


        print("s", end="")
        # print(stat, arrival, departure, platform)

        station_name = stat[0].find("a").text
        if "(" in station_name:
            station_name = station_name.split("(")[0].strip(" ")
        if "/" in station_name:
            station_name = station_name.split("/")[0].strip(" ")
        station_link = stat[0].find("a")["href"]
        station_arrival = arrival[0].text.strip("\n").strip("an ")
        station_departure = departure[0].text.strip("\n").strip("ab ")
        station_platform = platform[0].text.strip("\n").strip("Gleis ")

        df = pd.concat([df, pd.DataFrame([[station_name, station_link, station_arrival, station_departure, station_platform, train]], 
                                         columns=["station", "link", "arrival", "departure", "platform", "train"])])

    return df


# URL for the Deutsche Bahn travel information page
urls = [
    "https://reiseauskunft.bahn.de/bin/traininfo.exe/dn/12882/345834/275180/133300/80?ld=43110&protocol=https:&rt=1&date=23.01.24&time=10:36&station_evaId=8100514&station_type=dep&", # S1
    "https://reiseauskunft.bahn.de/bin/traininfo.exe/dn/826602/617147/893152/171043/80?ld=43110&country=DEU&protocol=https:&rt=1&date=23.01.24&time=10:39&station_evaId=8100514&station_type=dep&", # S2
    "https://reiseauskunft.bahn.de/bin/traininfo.exe/dn/496026/506790/213148/58771/80?ld=43110&country=DEU&protocol=https:&rt=1&date=23.01.24&time=10:33&station_evaId=8100514&station_type=dep&", # S3
    "https://reiseauskunft.bahn.de/bin/traininfo.exe/dn/43638/356659/116694/43801/80?ld=43110&protocol=https:&rt=1&date=23.01.24&time=07:32&station_evaId=8101590&station_type=dep&", # S4
    "https://reiseauskunft.bahn.de/bin/traininfo.exe/dn/396078/473927/954328/345138/80?ld=43110&country=DEU&protocol=https:&rt=1&date=23.01.24&time=11:36&station_evaId=8100236&station_type=dep&", # S7
    "https://reiseauskunft.bahn.de/bin/traininfo.exe/dn/770187/598545/821348/153949/80?ld=43110&protocol=https:&rt=1&date=23.01.24&time=09:36&station_evaId=8100516&station_type=dep&", # S60
    "https://reiseauskunft.bahn.de/bin/traininfo.exe/dn/797262/607398/899794/184148/80?ld=43110&country=DEU&protocol=https:&rt=1&date=23.01.24&time=10:41&station_evaId=8100514&station_type=dep&", # S80
    "https://reiseauskunft.bahn.de/bin/traininfo.exe/dn/15267/370211/305990/147918/80?ld=43110&country=DEU&protocol=https:&rt=1&date=16.01.24&time=12:42&station_evaId=8170059&station_type=dep&rtMode=&", # U1
    "https://reiseauskunft.bahn.de/bin/traininfo.exe/dn/650685/584800/128912/152441/80?ld=43110&protocol=https:&rt=1&date=16.01.24&time=13:27&station_evaId=8170049&station_type=dep&rtMode=&", # U2
    "https://reiseauskunft.bahn.de/bin/traininfo.exe/dn/395814/500381/527964/132059/80?ld=43110&protocol=https:&rt=1&date=16.01.24&time=13:24&station_evaId=8170024&station_type=dep&rtMode=&", #U3
    "https://reiseauskunft.bahn.de/bin/traininfo.exe/dn/466212/520367/666886/178076/80?ld=43110&protocol=https:&rt=1&date=16.01.24&time=13:28&station_evaId=8170248&station_type=dep&rtMode=&", # U4
    "https://reiseauskunft.bahn.de/bin/traininfo.exe/dn/958488/685362/708710/34873/80?ld=43110&country=DEU&protocol=https:&rt=1&date=23.01.24&time=10:21&station_evaId=8170040&station_type=dep&", # U6
    "https://reiseauskunft.bahn.de/bin/traininfo.exe/dn/292077/463807/856688/330986/80?ld=43110&country=DEU&protocol=https:&rt=1&date=16.01.24&time=13:30&station_evaId=8100394&station_type=dep&rtMode=&" # STR 18
]

df = pd.DataFrame(columns=["station", "link", "arrival", "departure", "platform", "train"])

for url in urls:
    # Scrape the data
    df = scrape_db_station_info(url, df = df)
    
df.to_csv("train_data.csv", index=False)

