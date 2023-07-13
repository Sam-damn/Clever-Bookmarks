from rest_framework.response import Response
from rest_framework import status
from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer
from rest_framework.decorators import api_view


def _get_bookmark(url):
    bookmark = Bookmark.objects.get(url=url)
    return bookmark

@api_view(['GET'])
def bookmarks_list(request):
    """
         API Controller to list all avaiable bookmarks or create a new one
    
    """
    bookmarks = Bookmark.objects.all()
    bookmarkSerializer = BookmarkSerializer(bookmarks, many=True)
    return Response(bookmarkSerializer.data)


@api_view(['GET', 'DELETE', 'PUT'])
def bookmark_controller(request, url):
    """
        API for handling CRUD actions for bookmarks
    
    """
    try: 
       bookmark =  _get_bookmark(url=url)
    except Bookmark.DoesNotExist:
        return Response("requested Bookmark was not found")

    if request.method == 'GET':
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data)
    
    elif request.method == 'PUT' : 
        serializer = BookmarkSerializer(bookmark)
        serializer.update(bookmark, request.query_params)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        bookmark.delete()
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data)

