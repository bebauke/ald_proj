import requests

class StationAPI:
    def __init__(self, base_url):
        """
        Initialize the StationAPI class.

        Args:
            base_url (str): The base URL for the API.
        """
        self.base_url = base_url

    def get_health(self):
        """
        Get the health status of the API.

        Returns:
            str: The health status of the API.
        """
        response = requests.get(f"{self.base_url}/health")
        
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()  # Raise an exception for non-200 status codes


    def get_station_by_id(self, id):
        """
        Get a specific station by its ID.

        Args:
            id (str): The ID of the station.

        Returns:
            dict: The station with the given ID.
        """
        response = requests.get(f"{self.base_url}/stations/{id}")
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()

    def get_reachable_from(self, id):
        """
        Get all stations reachable from a specific station.

        Args:
            id (str): The ID of the station.

        Returns:
            list: A list of all stations reachable from the given station.
        """
        response = requests.get(f"{self.base_url}/{id}")
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()
