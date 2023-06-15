from fastapi import HTTPException
from bson.objectid import ObjectId
from pymongo.database import Database
from datetime import datetime
import random
import string


class ShanyraksRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, shanyrak_data: dict, location: dict):
        payload = {
            "user_id": ObjectId(user_id),
            "type": shanyrak_data["type"],
            "price": shanyrak_data["price"],
            "address": shanyrak_data["address"],
            "area": shanyrak_data["area"],
            "rooms_count": shanyrak_data["rooms_count"],
            "description": shanyrak_data["description"],
            "location": location,
        }
        response = self.database["shanyraks"].insert_one(payload)
        return response.inserted_id

    def get_shanyrak_by_id(self, id: str):
        response = self.database["shanyraks"].find_one({"_id": ObjectId(id)})
        if response:
            return response
        else:
            raise HTTPException(status_code=404, detail="Element not found")

    def edit_shanyrak_by_id(self, id: str, user_id: str, input: dict):
        check_exist = self.database["shanyraks"].find_one(
            {"$and": [{"_id": ObjectId(id)}, {"user_id": ObjectId(user_id)}]}
        )
        if check_exist:
            response = self.database["shanyraks"].update_one(
                {"$and": [{"_id": ObjectId(id)}, {"user_id": ObjectId(user_id)}]},
                {
                    "$set": {
                        "type": input["type"],
                        "price": input["price"],
                        "address": input["address"],
                        "area": input["area"],
                        "rooms_count": input["rooms_count"],
                        "description": input["description"],
                    }
                },
            )
        else:
            raise HTTPException(status_code=404, detail="Element not found")

        return response

    def delete_shanyraq_by_id(self, id: str, user_id: str):
        check_exist = self.database["shanyraks"].find_one(
            {"$and": [{"_id": ObjectId(id)}, {"user_id": ObjectId(user_id)}]}
        )
        if check_exist:
            self.database["shanyraks"].delete_one({"_id": ObjectId(id)})
        else:
            raise HTTPException(status_code=404, detail="No permission")

    def create_comment_by_id(self, id: str, user_id: str, content: dict):
        check_exist = self.database["shanyraks"].find_one({"_id": ObjectId(id)})
        payload = {
            "comment_id": "".join(random.choices(string.ascii_lowercase, k=10)),
            "content": content["content"],
            "created_at": str(datetime.now()),
            "author_id": ObjectId(user_id),
        }
        if check_exist:
            self.database["shanyraks"].update_one(
                {"_id": ObjectId(id)}, {"$push": {"comments": payload}}
            )
        else:
            raise HTTPException(status_code=404, detail="Shanyrak does not exist")

    def get_comments(self, id: str):
        check_exist = self.database["shanyraks"].find_one({"_id": ObjectId(id)})

        if check_exist:
            response = self.database["shanyraks"].find_one({"_id": ObjectId(id)})
            if response:
                comments = response["comments"]
                return comments
            else:
                return []
        else:
            raise HTTPException(status_code=404, detail="Shanyrak does not exist")

    def edit_comment(self, id: str, comment_id: str, user_id: str, comment: dict):
        check_shanyrak_exist = self.database["shanyraks"].find_one(
            {"_id": ObjectId(id)}
        )

        if check_shanyrak_exist:
            check_comment_exist = self.database["shanyraks"].find_one(
                {
                    "$and": [
                        {"comments.comment_id": comment_id},
                        {"comments.author_id": ObjectId(user_id)},
                    ]
                }
            )

            if check_comment_exist:
                self.database["shanyraks"].update_one(
                    {
                        "$and": [
                            {"_id": ObjectId(id)},
                            {"comments.comment_id": comment_id},
                            {"comments.author_id": ObjectId(user_id)},
                        ]
                    },
                    {"$set": {"comments.$.content": comment["content"]}},
                )
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Comment does not exist, or cannot edit someone's comment",
                )
        else:
            raise HTTPException(status_code=404, detail="Shanyrak does not exist")

    def delete_comment(self, id: str, user_id: str, comment_id: str):
        check_shanyrak_exist = self.database["shanyraks"].find_one(
            {"_id": ObjectId(id)}
        )

        if check_shanyrak_exist:
            check_comment_exist = self.database["shanyraks"].find_one(
                {
                    "$and": [
                        {"comments.comment_id": comment_id},
                        {"comments.author_id": ObjectId(user_id)},
                    ]
                }
            )
            if check_comment_exist:
                self.database["shanyraks"].update_one(
                    {"_id": ObjectId(id)},
                    {
                        "$pull": {
                            "comments": {
                                "$and": [
                                    {"comment_id": comment_id},
                                    {"author_id": ObjectId(user_id)},
                                ]
                            }
                        }
                    },
                )
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Comment does not exist, or cannot delete someone's comment",
                )

        else:
            raise HTTPException(status_code=404, detail="Shanyrak does not exist")

    def upload_images(self, id: str, user_id: str, image_url: str):
        check_shanyrak_exist = self.database["shanyraks"].find_one(
            {"$and": [{"_id": ObjectId(id)}, {"user_id": ObjectId(user_id)}]}
        )

        if check_shanyrak_exist:
            self.database["shanyraks"].update_one(
                {"$and": [{"_id": ObjectId(id)}, {"user_id": ObjectId(user_id)}]},
                {"$push": {"media": image_url}},
            )
        else:
            raise HTTPException(
                status_code=404,
                detail="Shanyrak does not exist, or you cannot upload images to others posts",
            )

    def delete_images(self, id: str, user_id: str, image_url: str):
        check_shanyrak_exist = self.database["shanyraks"].find_one(
            {"$and": [{"_id": ObjectId(id)}, {"user_id": ObjectId(user_id)}]}
        )

        if check_shanyrak_exist:
            self.database["shanyraks"].update_one(
                {"$and": [{"_id": ObjectId(id)}, {"user_id": ObjectId(user_id)}]},
                {"$pull": {"media": image_url}},
            )
        else:
            raise HTTPException(
                status_code=404,
                detail="Shanyrak does not exist, or you cannot delete images to others posts",
            )
