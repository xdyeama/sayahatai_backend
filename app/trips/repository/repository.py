from datetime import datetime
from bson.objectid import ObjectId
from pymongo.database import Database
from typing import List
from fastapi import HTTPException


class TripsRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_trip(self, user_id: str, input: List):
        trip = {
            'user_id': ObjectId(user_id),
            "trip": input,
        }
        trip_id = self.database.trips.insert_one(trip).inserted_id
        return trip_id
    
    def get_trips(self, user_id: str) -> dict | None:
        does_trips_exist = self.database.trips.find({'user_id': ObjectId(user_id)})
        if does_trips_exist:
            trips = self.database.trips.find({'user_id': ObjectId(user_id)})
            return trips
        else:
            return None


