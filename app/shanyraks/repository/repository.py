from fastapi import HTTPException
from bson.objectid import ObjectId
from pymongo.database import Database
from datetime import datetime
import random
import string


class ShanyraksRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, shanyrak: dict, coordinates: dict):
        payload = {
            "type": shanyrak["type"],
            "price": shanyrak["price"],
            "address": shanyrak["address"],
            "area": shanyrak["area"],
            "rooms_count": shanyrak["rooms_count"],
            "description": shanyrak["description"],
            "location": {
                "latitude": coordinates["lat"],
                "longitude": coordinates["lng"],
            },
            "user_id": ObjectId(user_id),
        }
        new_shanyrak = self.database["shanyraks"].insert_one(payload)
        return new_shanyrak.inserted_id

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

    def get_filtered_shanyraks(
        self,
        limit: int,
        offset: int,
        type: str | None,
        rooms_count: int | None,
        price_from: int | None,
        price_until: int | None,
        latitude: float | None,
        longitude: float | None,
        radius: float | None,
    ):
        def get_query_filter(
            query_filter: dict,
            type: str | None,
            rooms_count: int | None,
            price_from: int | None,
            price_until: int | None,
            latitude: float | None,
            longitude: float | None,
            radius: float | None,
        ):
            if type is not None:
                query_filter["type"] = type
            if rooms_count is not None:
                query_filter["rooms_count"] = rooms_count
            price_filter = {}
            if price_from is not None:
                price_filter["$gte"] = price_from
            if price_until is not None:
                price_filter["$lte"] = price_until
            if price_filter != {}:
                query_filter["price"] = (price_filter,)
            if latitude is not None and longitude is not None and radius is not None:
                radius_converted_approximately = radius * 3.2535313808
                query_filter["location"] = {
                    "$geoWithin": {
                        "$centerSphere": [
                            [longitude, latitude],
                            radius_converted_approximately,
                        ]
                    }
                }
            return query_filter

        response_count = 0
        query_filter = get_query_filter(
            {},
            type,
            rooms_count,
            price_from,
            price_until,
            latitude,
            longitude,
            radius,
        )
        if limit == 0 and offset == 0:
            response = self.database["shanyraks"].find(query_filter)
            response_count = self.database["shanyraks"].count_documents({})
        else:
            response = (
                self.database["shanyraks"].find(query_filter).limit(limit).skip(offset)
            )

            response_count = self.database["shanyraks"].count_documents(query_filter)

        response_list = []
        for shanyrak in response:
            response_list.append(
                {
                    "_id": str(shanyrak["_id"]),
                    "type": shanyrak["type"],
                    "rooms_count": shanyrak["rooms_count"],
                    "address": shanyrak["address"],
                    "price": shanyrak["price"],
                    "area": shanyrak["area"],
                    "location": shanyrak["location"],
                }
            )
        return {"total": response_count, "items": response_list}
