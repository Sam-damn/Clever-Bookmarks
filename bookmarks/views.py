from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer

@csrf_exempt
def bookmarks_list(request):
    """
    API Controller to list all avaiable bookmarks or create a new one
    
    """
    if request.method == "GET":
        bookmarks = Bookmark.objects.all()
        bookmarkSerializer = BookmarkSerializer(bookmarks, many=True)
        return JsonResponse(bookmarkSerializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        bookmarkSerializer = BookmarkSerializer(data=data)
        if bookmarkSerializer.is_valid():
            bookmarkSerializer.save()
            return JsonResponse(data=bookmarkSerializer.data, status=201)
        return JsonResponse(bookmarkSerializer.errors, status=400)


        

