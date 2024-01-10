from flask import render_template

class MapboxFilterControl:
    def __init__(self, entries, default_entry, on_change):
        self.entries = entries
        self.default_entry = default_entry
        self.on_change = on_change

    def get_default_position(self):
        return 'top-right'

    def render(self):
        active_entry = next((e for e in self.entries if e.get('isActive')), None)
        active_is_default = active_entry and (active_entry.get('id') == self.default_entry)

        return render_template(
            'mapbox_filter_control.html',
            entries=self.entries,
            default_entry=self.default_entry,
            active_is_default=active_is_default
        )
