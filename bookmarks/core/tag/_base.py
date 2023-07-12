from typing import List
from collections import namedtuple
from typing import Optional

Tag = namedtuple('Tag', ['name', 'from_url'])

class BaseTagger():
    """ Base Tagger used for extracting tags for URL bookmarks """

    def __init__(self):
        pass

    def extract(self, url: str, content: Optional[str] = None) -> List[Tag]:
        """ get tags from a url """
        pass

    def get_tags(self, urls: List[str], contents: Optional[List[str]] = None) -> List[Tag]:
        tags = []
        if contents is not None:

            if len(urls) != len(contents):
                raise ValueError(
                    " Please ensure that `contents` and `urls` are of the same length! \n ")
            
            tags = [self.extract(url, content) for url,content in zip(urls, contents)]

        else :
            
            tags = [self.extract(url, None) for url in urls]

        return tags

