import requests
from fastapi import HTTPException


class HereService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_location(self, address: str):
        url = f"https://geocode.search.hereapi.com/v1/geocode?q={address}&apiKey={self.api_key}"

        response = requests.get(url)
        json = response.json()

        if "items" in json and len(json["items"]) > 0:
            return json["items"][0]["location"]
        else:
            raise HTTPException(status_code=404, detail="No address found")
