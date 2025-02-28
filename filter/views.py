from django.http import JsonResponse
from .helper import get_mongo_collection, filter_by_tags
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def filter_view(request):
    """
    Handles filtering of posts or questions by tags.

    Query Parameters:
        type: 'post' or 'question'
        tags: List of tags to filter by (e.g., ?tags=python&tags=django).

    Returns:
        JSON response containing a list of IDs.
    """
    content_type = request.GET.get("type")  # 'post' or 'question'
    tags = request.GET.getlist("tags")  # List of tags (e.g., ['python', 'django'])

    if not content_type or content_type not in ["post", "question"]:
        return JsonResponse({"error": "Invalid or missing content type"}, status=400)

    if not tags:
        return JsonResponse({"error": "No tags provided"}, status=400)

    # Get the appropriate collection from MongoDB
    collection = get_mongo_collection(content_type)
    if not collection:
        return JsonResponse({"error": "Failed to access collection"}, status=500)

    # Filter by tags and return IDs
    ids = filter_by_tags(collection, tags)
    return JsonResponse({"ids": ids}, safe=False)
