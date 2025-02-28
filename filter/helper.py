from pymongo import MongoClient
from django.conf import settings

def get_mongo_collection(content_type):
    """
    Connect to MongoDB and return the appropriate collection.
    """
    mongo_client = MongoClient(settings.MONGO_URI)
    db = mongo_client[settings.MONGO_DB_NAME]

    if content_type == "post":
        return db["posts"]  # MongoDB collection for posts
    elif content_type == "question":
        return db["questions"]  # MongoDB collection for questions
    else:
        return None

def filter_by_tags(collection, tags):
    """
    Filter documents in the given MongoDB collection by partially matching tags.

    Args:
        collection: MongoDB collection to query.
        tags: List of tags to filter by.

    Returns:
        List of IDs matching the tags.
    """
    # MongoDB query to check if any of the provided tags exist in the document's tags
    query = {"tags": {"$in": tags}}  # At least one tag matches
    projection = {"_id": 1}  # Only retrieve the `_id` field
    results = collection.find(query, projection)

    # Convert MongoDB ObjectId to string for JSON serialization
    return [str(result["_id"]) for result in results]
