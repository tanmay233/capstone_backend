from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import helper

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            # FIRST GET ALL THE FIELDS
            data = json.loads(request.body)
            username = data.get('username')
            firstname = data.get('firstname')
            lastname = data.get('lastname')
            designation = data.get('designation')
            email = data.get('email')
            password = data.get('password')
            reg_number = data.get('reg_number')
            
            # CHECK IF ALL THE FIELDS ARE PRESENT
            if not all([username, firstname, lastname,designation, email, password, reg_number]):
                return JsonResponse({"error": "All fields are required"}, status=400)
            
            # GET THE RESULT AFTE WE RUN THE SIGN UP API
            result = helper.Signup(username, firstname, lastname,designation, email, password, reg_number)
            return JsonResponse(result)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
        
# FUNCTION TO VERIFY THAT THE USER CAN LOGIN OR NOT IF LOG IN THEN DO ALL THAT MENTIONED IN THE HELPER.SIGNIN FUNCTION
@csrf_exempt
def login(request):
    if request.method == 'GET':
        try:
            data = json.loads(request.body)
            reg_number = data['reg_number']
            password = data['password']
            time = data['time']
            
            if not all([reg_number, password, time]):
                return JsonResponse({"error": "All fields are required"}, status=400)
                
            result = helper.Signin(reg_number, password, time)
            return JsonResponse(result)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    
@csrf_exempt
def logout(request):
    if request.method == 'GET':
        try:
            data = json.loads(request.body)
            token = data['token']
            reg_number = data['reg_number']
            
            if not all([token, reg_number]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            result = helper.Logout(token,reg_number)
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
            
#  FUNCTION TO UPDATE DETAILS OF A PERSON
@csrf_exempt
def update(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            reg_number = data.get('reg_number')
            toupdate = data.get('toupdate')
            
            if not all([token, reg_number, toupdate]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            result = helper.update(token, reg_number, toupdate)
            return JsonResponse(result)  # Ensure the result is returned as JsonResponse

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=500)  # Return the error as JsonResponse
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
        
                