import json
import pymongo
import jwt
import os
import base64
from datetime import datetime
from bson.objectid import ObjectId

from user.helper import validate_token

url = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(url)

database = client.get_database('testDB')
user_collection = database.get_collection('User')
token_collection = database.get_collection('Tokens')
question_collection = database.get_collection('Question')

def post_question(token, reg_number, title, content,comment_id,  tags = None):
    try:
        # WE HAVE GENERATED A QUESTION ID TO UNIQUELY IDENTIFY THE QUESTION
        question_id = str(ObjectId())  # Generate a unique question ID
        question_data = {
            "reg_number": reg_number,
            "question_id": question_id,
            "title": title,
            "content": content,
            "likes": 0,
            "tags": tags if tags else [],
            "comment_id" : comment_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        if validate_token(token, reg_number):
            result = question_collection.insert_one(question_data)
            
            if result.inserted_id:
                return {"success": f"Question posted successfully with ID {question_id}"}
            else:
                return {"error": "Failed to post the question"}
        else:
            return {'error' : 'Token not valid'}
    except Exception as e:
        return {"error": str(e)}
    
# FUNCTION TO UPDATE THE QUESTION DETAILS
def update_question(token, reg_number, question_id, updatedata):
    try:
        if validate_token(token, reg_number):
            question = question_collection.find_one({'question_id' : question_id})
            if not question:
                return {"error": "Question not found or you don't have permission to update this question"}
            updatedata['updated_at'] = datetime.now()
            result = question_collection.update_one({"question_id" : question_id}, {'$set' : updatedata})
            if result.modified_count > 0:
                return {"success": f"Question with ID {question_id} updated successfully"}
            else:
                return {"error": "No changes made to the question"}
        else:
            return {'error' : 'Invalid or Expired token'}
    except Exception as e:
        return {'error' : str(e)}
    
# FUNCTION TO DELETE A QUESTION
def  delete_question(token, reg_number, question_id):
    try:
        if validate_token(token, reg_number):
            result = question_collection.find_one({'question_id' : question_id})
            if not result:
                    return {"error": "Question not found or you don't have permission to delete this question"}
            result = question_collection.delete_one({"question_id": question_id})
            
            if result.deleted_count > 0:
                return {"success": f"Question with ID {question_id} deleted successfully"}
            else:
                return {"error": "Failed to delete the question"}
        else:
            return {"error": "Invalid or expired token"}
    except Exception as e:
        return {"error": str(e)}