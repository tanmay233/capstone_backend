import json
import pymongo
import jwt
import os
import base64
from bson import ObjectId

from user.helper import validate_token

url = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(url)

database = client.get_database('testDB')
user_collection = database.get_collection('User')
token_collection = database.get_collection('Tokens')
comment_collection = database.get_collection('Comment')


def add_comment(token, question_id, title, content, reg_number, qptype):
    try:
        # Validate the token
        if validate_token(token, reg_number):
            comment_id = str(ObjectId())  # Create a unique ID for the comment
            query = {
                "comment_id": comment_id,
                "question_id": question_id,
                "title": title,
                "content": content,
                "reg_number": reg_number,
                "upvotes": 0,
                "type": qptype
            }
            result = comment_collection.insert_one(query)
            if result.inserted_id:
                return {"success": f"Comment added successfully with ID {comment_id}"}
            else:
                return {"error": "Failed to add comment"}
        else:
            return {"error": "Invalid token"}
    except Exception as e:
        return {"error": str(e)}