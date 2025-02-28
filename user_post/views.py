from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import helper

@csrf_exempt
def post_question(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['token']
            reg_number = data['reg_number']
            title = data['title']
            content = data.get('content', {})
            tags = data.get('tags', [])
            comment_id = data.get('comment_id', [])
            
            if not all([token, reg_number, title, content]):
                return JsonResponse({"error": "Token, title, and content are required"}, status=400)
            
            result = helper.post_question(token, reg_number, title, content, comment_id, tags)
            return JsonResponse(result)
            
        except Exception as e:
            return JsonResponse({'error' : str(e)})
        
@csrf_exempt
def update_question(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            token = data['token']
            question_id = data['question_id']
            updatedata = data.get('updatedata', {})
            
            if not all ([token, question_id, updatedata]):
                return JsonResponse({"error": "Token, question_id, and fields to update are required"}, status=400)
            result = helper.update_question(token, question_id, updatedata)
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    
@csrf_exempt
def delete_question(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            question_id = data.get('question_id')
            
            if not all([token, question_id]):
                return JsonResponse({'error' : 'Token, question_id are required'}, status=400)
            result = helper.delete_question(token, question_id)
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)