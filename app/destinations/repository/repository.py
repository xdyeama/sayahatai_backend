from bson.objectid import ObjectId
from pymongo.database import Database


class DestinationRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_destination(self, title: str, address: str, location: dict):
        destination = {
            "title": title,
            "address": address,
            "location": location
        }
        self.database["destination"].insert_one(destination)

    def get_all_destinations(self):
        return self.database["destination"].find()
    
    def get_destination_by_id(self, destination_id: ObjectId):
        return self.database["destination"].find_one({"_id": ObjectId(destination_id)})
    

    