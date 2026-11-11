from datetime import datetime, timezone

import motor.motor_asyncio
from bson import ObjectId
from pymongo import ReturnDocument

from info import DATABASE_NAME, USER_DB_URI


class TitleRequests:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(USER_DB_URI)
        self.collection = self.client[DATABASE_NAME].title_requests

    async def add(self, title, user_id):
        request = {
            "title": title,
            "user_id": int(user_id),
            "status": "open",
            "created_at": datetime.now(timezone.utc),
        }
        result = await self.collection.insert_one(request)
        return str(result.inserted_id)

    async def get_open(self, skip=0, limit=5):
        cursor = (
            self.collection.find({"status": "open"})
            .sort("created_at", 1)
            .skip(skip)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)

    async def get_user_requests(self, user_id, limit=5):
        cursor = (
            self.collection.find({"user_id": int(user_id)})
            .sort("created_at", -1)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)

    async def mark_fulfilled(self, request_id):
        if not ObjectId.is_valid(request_id):
            return None
        return await self.collection.find_one_and_update(
            {"_id": ObjectId(request_id), "status": "open"},
            {
                "$set": {
                    "status": "fulfilled",
                    "fulfilled_at": datetime.now(timezone.utc),
                }
            },
            return_document=ReturnDocument.BEFORE,
        )


title_requests = TitleRequests()
