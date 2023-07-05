from bson.objectid import ObjectId
from pymongo.database import Database
from typing import List
from fastapi import HTTPException


class TripsRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_trip(self, user_id: str, input: List):
        trip = {
            "user_id": ObjectId(user_id),
            "trip": input,
        }
        trip_id = self.database.trips.insert_one(trip).inserted_id
        return trip_id

    def get_trips(self, user_id: str) -> dict | None:
        does_trips_exist = self.database.trips.find({"user_id": ObjectId(user_id)})
        if does_trips_exist:
            trips = self.database.trips.find({"user_id": ObjectId(user_id)})
            return trips
        else:
            return None

    def get_trip_by_id(self, user_id: str, trip_id: str) -> dict | None:
        does_trip_exist = self.database.trips.find_one({"user_id": ObjectId(user_id)})

        if does_trip_exist:
            trip = self.database.trips.find_one(
                {"user_id": ObjectId(user_id), "_id": ObjectId(trip_id)}
            )
            return trip
        else:
            raise HTTPException(status_code=404, detail="Such trip does not exist")

    def edit_trip(self, user_id: str, trip_id: str, input: dict):
        does_trip_exist = self.database.trips.find_one(
            {"_id": ObjectId(trip_id), "user_id": ObjectId(user_id)}
        )

        if does_trip_exist:
            does_day_plan_exist = self.database.trips.find_one(
                {
                    "_id": ObjectId(trip_id),
                    "user_id": ObjectId(user_id),
                    "trip.day_num": input["day_num"],
                }
            )

            if does_day_plan_exist:
                self.database.trips.update_one(
                    {
                        "_id": ObjectId(trip_id),
                        "user_id": ObjectId(user_id),
                        "trip.day_num": input["day_num"],
                    },
                    {
                        "$set": {
                            "trip.$.day_num": input["day_num"],
                            "trip.$.city": input["city"],
                            "trip.$.activities": input["activities"],
                        }
                    },
                )
            else:
                raise HTTPException(
                    status_code=404, detail="Such daily plan does not exist"
                )
        else:
            raise HTTPException(status_code=404, detail="Such trip does not exist")

    def delete_trip(self, user_id: str, trip_id: str):
        does_trip_exist = self.database.trips.find_one(
            {"_id": ObjectId(trip_id), "user_id": ObjectId(user_id)}
        )

        if does_trip_exist:
            self.database.trips.delete_one(
                {"_id": ObjectId(trip_id), "user_id": ObjectId(user_id)}
            )
        else:
            raise HTTPException(status_code=404, detail="Such trip does not exist")
