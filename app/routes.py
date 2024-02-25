from app import app
from flask import render_template
import folium

from app.helpers.mapbox_filter_controles import MapboxFilterControl
from app.helpers.map import Map_Template

from flask import send_from_directory

@app.route('/mapbox')
def mapbox():
    return send_from_directory('static', 'map.html')

from flask import Flask, request, jsonify
from app.helpers.calc import calculate_shortest_route_and_stats

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    start = data['start']
    end = data['end']
    algorithm = data['algorithm']

    # Rufen Sie die Funktion auf, die die kürzeste Route und die Suchstatistiken berechnet
    shortest_route, search_stats = calculate_shortest_route_and_stats(start, end, algorithm)

    # TODO: Create the map : is done in calculte_shortest_route_and_stats


    # Senden Sie die Ergebnisse zurück an den Client
    return jsonify({
        'shortest_route': shortest_route,
        'search_stats': search_stats
    })  


@app.route('/')
def index():
    mapbox_filter_control = MapboxFilterControl(
        entries=[
            {'id': 'start', 'title': 'Von', 'isActive': True},
            {'id': 'end', 'title': 'Nach', 'isActive': True},
            # Add more entries as needed
        ],
        default_entry='start',
        on_change=lambda selected_entry: print(f'Selected entry: {selected_entry}')
    )

    return render_template('index.html', mapbox_filter_control=mapbox_filter_control, map = Map_Template())   

