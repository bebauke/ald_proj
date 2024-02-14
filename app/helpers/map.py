from flask import render_template
from app.helpers.calc import get_nodes

class Map_Template:
    def __init__(self):
        pass

    # def get_default_position(self):
    #     return 'top-right'

    def render(self):
        return render_template(
            'map.html'
        )
