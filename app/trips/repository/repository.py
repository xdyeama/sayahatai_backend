from datetime import datetime
from bson.objectid import ObjectId
from pymongo.database import Database


class TripsRepository:
    def __init__(self, database: Database):
        self.database = database

    # def create_trip(self, destinations: List(Destination)):
    #     trip = Trip(destinations=destinations)
    #     trip_id = self.database["trips"].insert_one(trip.dict())
    #     return trip_id.inserted_id
