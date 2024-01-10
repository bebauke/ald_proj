import requests
# from shapely.geometry import Point

class TransportHelpers:
    def __init__(self):
        self.en_locale = requests.get('https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/slim-3/slim-3.json').json()
        self.de_locale = requests.get('https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/slim-3/slim-3.de.json').json()

    def fetch_station(self, query):
        return requests.get(f'https://v5.db.transport.rest/locations?query={query}&poi=false&addresses=false').json()

    def format_station_id(self, i):
        return i[2:] if len(i) == 9 and i[:2] else i

    def country_for_station_id(self, i, language):
        i = self.format_station_id(i)
        if not self.is_uic_location_code(i):
            return None

        country_prefix = int(i[:2])
        alpha3 = self.to_iso[country_prefix]
        if not alpha3:
            return None

        return self.countries.get(alpha3, {}).get(language, alpha3)  # Using get to handle cases where the alpha3 is not found

    async def station_by_id(self, _id):
        candidates = await self.fetch_station(_id)
        formatted_id = self.format_station_id(_id)

        return next(
            (
                s
                for s in candidates
                if self.format_station_id(s['id']) == formatted_id and formatted_id and s['location']
            ),
            None
        )

    def location_to_point(self, location):
        raise NotImplementedError('location_to_point is not implemented')
        # return Point(location['longitude'], location['latitude'])

    def duration_category(self, d):
        if d == 0:
            return 0
        if not d:
            return -1
        if 0 < d <= 60:
            return 1
        if 0 < d <= 120:
            return 2
        if 0 < d <= 240:
            return 3
        if 0 < d <= 480:
            return 4
        if 0 < d <= 960:
            return 5
        return 6

    def duration_category_color(self, c):
        if c == -1:
            return '#999'  # unknown duration
        if c == 0:
            return '#333'  # 0
        if c == 1:
            return '#191'  # < 1h
        if c == 2:
            return '#2d1'  # 1h-2h
        if c == 3:
            return '#d4d411'  # 2h-4h
        if c == 4:
            return '#d91'  # 4h-8h
        if c == 5:
            return '#d41'  # 8h-16h
        if c == 6:
            return '#a41'  # > 16h
        return '#999'

    def to_point(self, language):
        def wrapper(station):
            return {
                'center': [station['location']['longitude'], station['location']['latitude']],
                'geometry': {
                    'type': 'Point',
                    'coordinates': [station['location']['longitude'], station['location']['latitude']],
                },
                'place_name': ', '.join(filter(None, [station['name'], self.country_for_station_id(station['id'], language)])),
                'place_type': ['coordinate'],
                'properties': {
                    'id': station['id'],
                    'name': station['name'],
                },
                'type': 'Feature',
            }

        return wrapper

    def is_long_distance_or_regional_or_suburban(self, s):
        return (
            s['products']
            and (
                s['products']['nationalExp']
                or s['products']['nationalExpress']
                or s['products']['national']
                or s['products']['regionalExp']
                or s['products']['regionalExpress']
                or s['products']['regional']
                or s['products']['suburban']
            )
            and self.is_uic_location_code(self.format_station_id(s['id']))
        )

    def is_region(self, s):
        return s['name'].upper() == s['name']

    def has_location(self, s):
        return 'location' in s

    def is_uic_location_code(self, i):
        return len(i) == 7 and i.isnumeric()  # Assuming a UIC location code is a 7-digit numeric string

    @property
    def to_iso(self):
        # Replace this with the actual implementation of toISO
        # For brevity, I'm providing a placeholder implementation
        return {80: 'DEU', 81: 'FRA', 82: 'ESP', 83: 'ITA'}

    @property
    def countries(self):
        # Replace this with the actual implementation of countries
        # For brevity, I'm providing a placeholder implementation
        return {'DEU': {'en': 'Germany', 'de': 'Deutschland'}, 'FRA': {'en': 'France', 'de': 'Frankreich'}}


# Example usage:
transport_helpers = TransportHelpers()
result = transport_helpers.station_by_id('8000207')
print(result)
