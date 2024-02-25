# ALD - Das ist der Weg 
<p align="center">
 <img width="50" height="50" src="app/static/images/favicon.png">
</p>

Dieses Projekt ist im Rahmen der Lehrveranstalltung ALD (WS24) an der FHOÖ in Wels entstanden. Das Projekt dient der Leistungserhebung für die Studenten Bauke und Malzer.

Die Anwendung ermöglicht einen einfachen Vergleich unterschiedlicher Suchalgorithmen, die dazu das `ISearchAlgorithm`-Interface erfüllen müssen. Bereits implementiert sind der Dijkstra- sowie der A*-Algorithmus. 

## 1. Bedienung
Nach dem Starten der run.py wird im Browser die Adresse [localhost Port 5000](http://localhost:5000/) ausgeführt Die Bedienung erfolgt über ein Webinterface, dass auf dem Flask-Framework aufgesetzt ist.
Über ein Drop-Down-Menü wird der zu verwendendende Suchalgorithmus ausgewählt. Zwei Textfelder dienen der Eingabe von Start und Endpunkt. Mögliche Optionen werden vorgeschlagen. 
Wenn die über den Button "Suche starten" gestartete Suche abgeschlossen ist, wird eine Statistik im unteren Teil der Seite angezeigt. So wird die Strecke des Pfades, die Dauer, die Anzahl der Knoten und die dauer der Suche selbst angezeigt. Darunter wird der kürzeste Pfad aufgelistet.

Die Karte visualisiert dabei, welche Knoten bei der Suche besucht wurden und welche den kürzesten Pfad bilden. 

![Benutzeroberfläche](<doc/img/img_ui.jpg> "Benutzeroberfläche")

## 2. Aufbau (Datenstuktur, Klassen)
### 2.1 User-Interface
Um den Pythoncode leicht bedienen zu können, wird Flask verwendet. Der Entrypoint ist dabei die datei `/run.py`. Die Ausgabe erfolgt dann auf [localhost Port 5000](http://localhost:5000/) als Development-Server. Für die Auslieferung sollte ein WSGI-Server aufgesetzt werden. 

Der Code für die Webanwendung befindet sich im Ordner `app`. Die Templates sind im Ordner `templates` und die statischen Dateien (CSS, JS, Bilder) im Ordner `static`. In der Datei `routes.py` sind die Routen definiert, die die Anfragen des Benutzers verarbeiten: 
- `/` - Startseite: Auswal der Parameter und Anzeige der Karte
- `/search` - Verarbeitung der Suchanfrage (Algorithmus ausführen, Karte aktualisieren)
- `/mapbox` - Addresse um die Karte zu laden

Durch das Betätigen der Schaltfläche "Suche starten" wird durch die JS-Funktion `search()` in der `index.html` die Anfrage als POST-Request an die Route `/search` gesendet. Die Antwort wird von `search()` verarbeitet, in das `div` mit der ID `result` geschrieben und die Karte neu geladen. 

In der Route `/search` werden die Parameter `start`, `end` und `algorithm` aus dem POST-Request ausgelesen und an den Helper `calculate_shortest_route_and_stats()` übergeben. Dieser berechnet abhängig vom gewählten Algorithmus den kürzesten Pfad und die Statistik. Ein weiterer Helper erstellt aus der Antwort des Algorithmus die Kartendarstellung und legt sie im Speicher ab. Dazu wird die Bibliothek `folium` verwendet.

Die Struktur des Projekts kann vereinfacht werden. So hätte ein einziges Template genügt, um die Oberfläche sowie die Karte darzustellen. Allerdings wurden hier verschiedene Konzepte von Flask verwendet, um die Möglichkeiten auszuloten. 

### 2.2 lib: Algorithmen und Datenstrukturen



### 2.3 Klassendiagramm
In folgendem Diagramm sind die wichtigsten Klassen und deren Beziehungen dargestellt.

![Klassendiagramm](<doc/img/img_class_diagram.jpg> "Klassendiagramm")


## 3. Logik (Algorithmus, Datenfluss, ...)

