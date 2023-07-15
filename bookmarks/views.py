from rest_framework.response import Response
from rest_framework import status
from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer
from rest_framework.decorators import api_view
from urllib.parse import unquote 

from bookmarks.tags.IntelligentTagger import IntelligentTagger

def _get_bookmark(encoded_url):
    url = unquote(encoded_url)
    bookmark = Bookmark.objects.get(url=url)
    return bookmark

@api_view(['GET', 'POST'])
def bookmarks_list(request):
    """
         API EndPoint for listing all available bookmarks or creating a new Bookmark
    
    """

    if request.method == "GET":

        bookmarks = Bookmark.objects.all()
        bookmarkSerializer = BookmarkSerializer(bookmarks, many=True)
        return Response(bookmarkSerializer.data)
    
    elif request.method == "POST": 
        serializer = BookmarkSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
def bookmark_controller(request, encoded_url):
    """
        API for handling CRUD actions on bookmarks
    
    """
    try: 
       bookmark =  _get_bookmark(encoded_url)
    except Bookmark.DoesNotExist:
        return Response("requested Bookmark was not found")

    if request.method == 'GET':
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data)
    
    elif request.method == 'PUT' : 
        serializer = BookmarkSerializer(bookmark)
        serializer.update(bookmark, request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        bookmark.delete()
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data)


@api_view(['GET'])
def tags(request):
    url = request.query_params['url']
    tagger = IntelligentTagger()
    tags = tagger.extract(url)
    tags_serializable = [tag._asdict() for tag in tags]
    return Response(tags_serializable)

