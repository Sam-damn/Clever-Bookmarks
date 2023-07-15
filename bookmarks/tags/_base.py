from typing import List
from collections import namedtuple
from typing import Optional

Tag = namedtuple('Tag', ['name', 'tag_method'])

class BaseTagger():
    """ Base Tagger used for extracting tags from a URL """

    def __init__(self, method: str):
        self.tagging_method = method
    
    def _to_tag(self, tag: str) -> Tag:
        return Tag(tag, self.tagging_method)
    
    def extract(self, url: str, content: Optional[str] = None) -> List[Tag]:
        """
            Main method used to get tags from a certain url 

            Implementation differs between different taggers
        """
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

