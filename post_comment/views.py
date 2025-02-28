import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from post_comment import helper

@csrf_exempt
def post_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            question_id = data.get('question_id')
            title = data.get('title')
            content = data.get('content', {})
            reg_number = data.get('reg_number'),
            qptype = data.get('qptype')

            if not all([token, question_id, title, content, reg_number]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            result = helper.add_comment(token, question_id, title, content, reg_number, qptype)
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
