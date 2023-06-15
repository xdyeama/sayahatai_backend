from datetime import datetime
from fastapi import HTTPException

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user

    def edit_user_by_id(self, user_id: str, userData: dict) -> dict | None:
        user = self.database["users"].update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "phone": userData["phone"],
                    "name": userData["name"],
                    "city": userData["city"],
                }
            },
        )

        return user

    def add_to_favourites(self, user_id: str, shanyrak: dict):
        self.database["users"].update_one(
            {"_id": ObjectId(user_id)}, {"$push": {"shanyraks": shanyrak}}
        )

    def get_favourites(self, user_id: str):
        response = self.database["users"].find_one({"_id": ObjectId(user_id)})
        if response["shanyraks"]:
            return response["shanyraks"]
        else:
            return []

    def delete_favourite(self, user_id: str, shanyrak_id: str):
        does_favourite_exist = self.database["users"].find_one(
            {"shanyraks._id": ObjectId(shanyrak_id)}
        )

        if does_favourite_exist:
            response = self.database["users"].update_one(
                {"_id": ObjectId(user_id)},
                {"$pull": {"shanyraks": {"_id": ObjectId(shanyrak_id)}}},
            )
            return response
        else:
            raise HTTPException(status_code=404, detail="Such favourite does not exist")

    def upload_avatar(self, user_id: str, avatar_url: str):
        self.database["users"].update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"avatar_url": avatar_url}}
        )

    def delete_avatar(self, user_id: str):
        user = self.database["users"].find_one({"_id": ObjectId(user_id)})
        if user["avatar_url"]:
            self.database["users"].update_one(
                {"_id": ObjectId(user_id)}, {"$set": {"avatar_url": ""}}
            )
        else:
            raise HTTPException(status_code=404, detail="No avatar image to delete")
