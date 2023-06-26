import requests


class HereService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_location(self, address):
        url = f"https://geocode.search.hereapi.com/v1/geocode?q={address}&apikey=zCvpK-ZyeEvYSzN0WsHUDrGCifTJvWK0u6rnBMkGmGE"
        response = requests.get(url)
        json = response.json()
        return json
