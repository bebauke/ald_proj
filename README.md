# ALD - Das ist der Weg 
<p align="center">![Mando](app/static/images/favicon.png?raw=true)</p>

Dieses Projekt ist im Rahmen der Lehrveranstalltung ALD (WS24) an der FHOÖ in Wels entstanden. Das Projekt dient der Leistungserhebung für die Studenten Bauke und Malzer.

Die Anwendung ermöglicht einen einfachen Vergleich unterschiedlicher Suchalgorithmen, die dazu das `ISearchAlgorithm`-Interface erfüllen müssen. Bereits implementiert sind der Dijkstra- sowie der A*-Algorithmus. 

## 1. Bedienung
Die Bedienung erfolgt über ein Webinterface, dass auf dem Flask-Framework aufgesetzt ist.
Über ein Drop-Down-Menü wird der zu verwendendende Suchalgorithmus ausgewählt. Zwei Textfelder dienen der Eingabe von Start und Endpunkt. Mögliche Optionen werden vorgeschlagen. 
Wenn die über den Button "Suche starten" gestartete Suche abgeschlossen ist, wird eine Statistik im unteren Teil der Seite angezeigt. So wird die Strecke des Pfades, die Dauer, die Anzahl der Knoten und die dauer der Suche selbst angezeigt. Darunter wird der kürzeste Pfad aufgelistet.

Die Karte visualisiert dabei, welche Knoten bei der Suche besucht wurden und welche den kürzesten Pfad bilden. 

## 2. Aufbau (Datenstuktur, Klassen)
### 2.1 Klassen


## 3. Logik (Algorithmus, Datenfluss, ...)

