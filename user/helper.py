import json
import pymongo
import jwt
import os
import base64

url = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(url)

database = client.get_database('testDB')
user_collection = database.get_collection('User')
token_collection = database.get_collection('Tokens')

SECRET_KEY = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8') 

# FUNCTION TO SIGN UP THE USER FOR THE FIRST TIME
def Signup(username, firstname, lastname, designation, email, password, reg_number):
    try:
        # CHECK IF THE USER HAS ALREADY REGISTERED USERNAME OR REG_NUMBER
        if user_collection.find_one({'username': username}):
            return {'error': 'Username already in use'}
        if user_collection.find_one({'reg_number': reg_number}):
            return {'error': 'Registration number alreagy registered'}
        
        # IF NO REGISTERTED USERNAME OR REG_NUMBER THE GO AHEAD AND RUN THE QUERY TO SIGNUP
        query = {
            "username": username,
            "firstname": firstname,
            "lastname": lastname,
            "designation" : designation,
            "email": email,
            "password": password,
            "reg_number": reg_number
        }
        
        result = user_collection.insert_one(query)
        
        # IF SOME ERROR ACCURED IN ENTERING THE DATA THEN RETURN THE ERROR
        if result.inserted_id:
          return {'success' : 'User registered successfully'}
        else:
            return {'error' : 'Registration Falied'}
    
    except Exception as e:
        return {'error' : str(e)}  
    
# FUNCTION TO LOGIN THE USER WHO HAS ALREADY REGISTERED WITH THE APP

def Signin(reg_number, password, time):
    try:
        # CHECK IF THERE IS A REGISTER USER WITH THE REGISTRAION NUMBER GIVEN
        user = user_collection.find_one({"reg_number" : reg_number})
        if user:
            # IF THERE IS A USER THEN CHECK IF THE PASSWORD SUPLIED IS CORRECT OR NOT
            if user['password'] == password:
                
                # ENCODING THE REGISTRATION NUMBER USING BASE 64 ENCODING
                payload = {
                    'reg_number' : reg_number,
                    'time' : time
                }
                json_data = json.dumps(payload)
                token = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
                # CHECK IF THERE IS ALREDY A REGISTERED TOKEN 
                existing_token = token_collection.find_one({'token' : token})
                # IF THERE IS A USER WITH A TOKEN THEN UPDATE THE TOKEN
                if existing_token:
                    token_collection.update_one(
                        {'reg_number' : reg_number},
                        {'$set' : {'token' : token}}
                    )
                else:
                    token_collection.insert_one({'reg_number' : reg_number, 'token' : token})
                
                return {'success' : 'Login successful' , 'token' : token}
            else:
                return {'error' : 'Passwrod is incorrect'}
        else:
            return {'error' : 'No user fond with the given registered number'}
    except Exception as e:
        return {'error' : str(e)}
    
# FUNCTION TO LOGOUT AND ALSO DESTROY THE TOKEN 

def Logout(token, reg_number):
    try:
        # TRY TO DELETE THE TOKEN 
        result = token_collection.delete_one({'token' : token})
        
        # IF THE DELETE COUNT IS > 0 THEN THE TOKEN IS DELETED AND SUCCESS
        if result.deleted_count > 0:
            return {'success' : f"User with the registration number {reg_number} logged out successfully"}
        else:
            return {'error' : 'Token not found or already logged out'}

    except Exception as e:
        return {'error' : str(e)}

# FUNCTION TO VALIDATE THE TOKEN FOR SOME UPDATION OF THING 
def validate_token(token, reg_number):
    try:
        # FIRST DECODE WHAT WE HAVE GOT
        # decoded_token = base64.b64decode(token).decode('utf-8')
        decoded_token = base64.b64decode(token)
        json_data = decoded_token.decode('utf-8')
        d = json.loads(json_data)
        # FIND THE ENTRY FOR THAT TOKEN
        found = token_collection.find_one({'token' : token})
        print(d['reg_number'])
        print(found['reg_number'])
        print(reg_number)
        if found:
            # IF THE REGISTRATION NUMBER MATCHES WITH THE TOKEN THEN THE TOKEN IS VALID 
            if d['reg_number'] == found['reg_number'] == reg_number[0]:
                return True
            else:
                return False
        else:
            return False
    except:
        return False
    
# FUNCTION TO UPDATE THE PASSWORD
def update(token, reg_number, data):
    try:
        if validate_token(token, reg_number):
            result = user_collection.update_one({'reg_number' : reg_number}, {'$set' : data})
            if result.matched_count > 0:
                return {"success": f"User with registration number {reg_number} updated successfully"}
            
            return {'error' : "User not found or no changes made"}
        else:
            return {'error': 'Invalid token'}
    
    except Exception as e:
        return {"error": str(e)}

    
            