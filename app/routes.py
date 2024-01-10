from app import app
from flask import render_template
import folium

from app.helpers.mapbox_filter_controles import MapboxFilterControl

@app.route('/')
def index():
    mapbox_filter_control = MapboxFilterControl(
        entries=[
            {'id': 'entry1', 'title': 'Entry 1', 'isActive': True},
            {'id': 'entry2', 'title': 'Entry 2', 'isActive': False},
            # Add more entries as needed
        ],
        default_entry='entry1',
        on_change=lambda selected_entry: print(f'Selected entry: {selected_entry}')
    )

    return render_template('index.html', mapbox_filter_control=mapbox_filter_control)

