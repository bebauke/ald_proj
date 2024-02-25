# ALD - Das ist der Weg 
<p align="center">
 <img width="50" height="50" src="app/static/images/favicon.png">
</p>

Dieses Projekt ist im Rahmen der Lehrveranstalltung ALD (WS24) an der FHOÖ in Wels entstanden. Das Projekt dient der Leistungserhebung für die Studenten Bauke und Malzer.

Die Anwendung ermöglicht einen einfachen Vergleich unterschiedlicher Suchalgorithmen, die dazu das `ISearchAlgorithm`-Interface erfüllen müssen. Bereits implementiert sind der Dijkstra- sowie der A*-Algorithmus. 

## Installation
Das Projekt wurde in Python 3.11 entwickelt. Dazu wurden die Bibliotheken `flask` und `folium` verwendet. Die Installation kann über pip in ein `.venv` erfolgen.
```shell
python -m venv .venv
.venv/bin/activate
pip install Flask folium
``` 
`geopy` wurde für die Adressenauflösung verwendet und wird nicht zwingend benötigt.
```shell
pip install geopy
```

## 1. Bedienung
Nach dem Starten der run.py wird im Browser die Adresse [localhost:5000](http://localhost:5000/) ausgeführt Die Bedienung erfolgt über ein Webinterface, dass auf dem Flask-Framework aufgesetzt ist.
Über ein Drop-Down-Menü wird der zu verwendendende Suchalgorithmus ausgewählt. Zwei Textfelder dienen der Eingabe von Start und Endpunkt. Mögliche Optionen werden vorgeschlagen. 
Wenn die über den Button "Suche starten" gestartete Suche abgeschlossen ist, wird eine Statistik im unteren Teil der Seite angezeigt. So wird die Strecke des Pfades, die Dauer, die Anzahl der Knoten und die dauer der Suche selbst angezeigt. Darunter wird der kürzeste Pfad aufgelistet.

Die Karte visualisiert dabei, welche Knoten bei der Suche besucht wurden und welche den kürzesten Pfad bilden. 

![Benutzeroberfläche](<doc/img/img_ui.jpg> "Benutzeroberfläche")

## 2. Aufbau (Datenstuktur, Klassen)
### 2.1 User-Interface

Der Code für die Webanwendung befindet sich im Ordner `app`. Die Templates sind im Ordner `templates` und die statischen Dateien (CSS, JS, Bilder) im Ordner `static`. In der Datei `routes.py` sind die Routen definiert, die die Anfragen des Benutzers verarbeiten: 
- `/` (index) - Startseite: Auswal der Parameter und Anzeige der Karte
- `/search` - Verarbeitung der Suchanfrage (Algorithmus ausführen, Karte aktualisieren)
- `/mapbox` - Addresse um die Karte zu laden

"Suche starten" führt die in der `index.html` definierte JS-Funktion `search()` aus, welche einen POST-Request mit den Parametern `start`, `end` und `algorithm` an die Route `/search` sendet. Die Antwort wird verarbeitet, in die `result`-Box geschrieben und die Karte neu geladen. 

Die Route `/search` leitet die Parameter an `calculate_shortest_route_and_stats()` weiter. Abhängig vom Algorithmus wird der kürzeste Pfad und die Statistik. Der `MapHelper` erstellt aus der Antwort des Such-Algorithmus die Kartendarstellung und legt sie im Speicher ab. Dazu wird die Bibliothek `folium` verwendet.

### 2.2 lib: Algorithmen und Datenstrukturen

Die Bibliothek `lib` enthält, eingeteilt in `algorithms` und `data` die Implementierungen der Suchalgorithmen und der Datenstrukturen, die für die Suche benötigt werden. Für die Suche wird ein Graph benötigt, der in der Klasse `Graph` implementiert ist. Die Knoten können dabei beliebig sein. In dieser Anwendung sind es `string`-Objekte, die die Namen der Knoten repräsentieren. Die Kanten sind hier ungerichtet und haben ein Gewicht, können aber durch die angabe eines weiteren Gewichts auch gerichtet genutzt werden.

Die Suchalgorithmen müssen das Interface `ISearchAlgorithm` erfüllen. Dieses besteht aus einer Methode `search(graph: Graph, start: str, end: str) -> Tuple[List[str], List[str]]`. Die Methode gibt den kürzesten Pfad und die besuchten Knoten zurück. 

Darüber hinaus finden sich in `lib` noch die Funktion `map_helper.py`, die eine Folium-Karte anhand der gefundenen Pfade zeichnet.

Zu guter Letzt gibt es noch weitere Funktioinen, die für die Datenallokation, die Tests und die Visualisierung der Daten benötigt wurden.


### 2.3 Klassendiagramm
In folgendem Diagramm sind die wichtigsten Klassen und deren Beziehungen dargestellt.
Dabei ist der `<<global scope>>` die Flask-App, die die Webanwendung steuert und in der Grafik rein informativ dargestellt ist.

![Klassendiagramm](<doc/img/img_class_diagram.jpg> "Klassendiagramm")


## 3. Logik (Algorithmus, Datenfluss, ...)

### 3.1 Algorithmus
Die Algorithmen, die in dieser Anwendung verwendet werden, sind der Dijkstra- und der A*-Algorithmus. Beide Algorithmen sind in der Klasse `Dijkstra` und `AStar` implementiert und erfüllen das `ISearchAlgorithm`-Interface.

Der Dijkstra- sowie der A*-Algorithmus wurden nach dem Skript von M. Zauner implementiert. Der Dijkstra-Algorithmus ist ein uninformierter Suchalgorithmus, der den kürzesten Pfad zwischen zwei Knoten in einem Graphen findet. Der A*-Algorithmus ist ein informierter Suchalgorithmus, der den kürzesten Pfad zwischen zwei Knoten in einem Graphen findet. Dabei wird die Distanz zwischen den Knoten und dem Ziel berücksichtigt.

Eine optimierte Variante des A*-Algorithmus wurde implementiert, welche auf eine Priority Queue zurückgreift. Durch die Verwendung einer Priority Queue werden die Knoten nicht in einer Liste, sondern in einer Queue gespeichert. Dies ermöglicht eine schnellere Suche, da die Knoten mit der geringsten Distanz zuerst besucht werden.

### 3.2 Datenfluss
Der Datenfluss beginnt mit der Eingabe der Parameter durch den Benutzer. Diese werden an die Flask-App gesendet und dort verarbeitet. Die Parameter werden an den Algorithmus weitergegeben, der den kürzesten Pfad und die Statistik zurückgibt. Die Karte wird anhand des kürzesten Pfades gezeichnet und dem Benutzer neben den Statistiken angezeigt.