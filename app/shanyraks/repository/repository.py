from fastapi import HTTPException
from bson.objectid import ObjectId
from pymongo.database import Database


class ShanyraksRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, shanyrak_data: dict):
        payload = {
            "user_id": ObjectId(user_id),
            "type": shanyrak_data["type"],
            "price": shanyrak_data["price"],
            "address": shanyrak_data["address"],
            "area": shanyrak_data["area"],
            "rooms_count": shanyrak_data["rooms_count"],
            "description": shanyrak_data["description"],
        }
        response = self.database["shanyraks"].insert_one(payload)
        return response.inserted_id
    
    def get_shanyrak_by_id(self, id: str):
        response = self.database["shanyraks"].find_one({'_id': ObjectId(id)})
        if response:
            return response
        else:
            raise HTTPException(status_code=404, detail="Element not found")
        
    def edit_shanyrak_by_id(self, id: str, user_id: str, input: dict):
        check_exist = self.database["shanyraks"].find_one(
            {
                '$and': [{'_id': ObjectId(id)}, {'user_id': ObjectId(user_id)}]
                })
        if check_exist:
            response = self.database["shanyraks"].update_one({
                '$and': [{'_id': ObjectId(id)}, {'user_id': ObjectId(user_id)}]
                }, {'$set': {
                    "type": input["type"],
                    "price": input["price"],
                    "address": input["address"],
                    "area": input["area"],
                    "rooms_count": input["rooms_count"],
                    "description": input["description"]
                }})
        else:
            raise HTTPException(status_code=404, detail="Element not found")
        
        return response
    
    def delete_shanyraq_by_id(self, id: str, user_id: str):
        check_exist = self.database["shanyraks"].find_one(
            {
                '$and': [{'_id': ObjectId(id)}, {'user_id': ObjectId(user_id)}]
            })
        if check_exist:
            self.database["shanyraks"].delete_one({"_id": ObjectId(id)})
        else:
            raise HTTPException(status_code=404, detail="No permission")


