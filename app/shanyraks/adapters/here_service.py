import requests


class HereService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_location(self, address: str):
        url = f"https://geocode.search.hereapi.com/v1/geocode?q={address}&apiKey={self.api_key}"

        response = requests.get(url)
        json = response.json()

        if "items" in json.keys() and json["items"] > 0:
            return {
                "latitude": json["items"][0]["location"]["lat"],
                "longitude": json["items"][0]["location"]["lng"],
            }
        else:
            return {"latitude": 0, "longitude": 0}
