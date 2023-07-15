from typing import List, Optional, Any

from bookmarks.lib.web_scraper import scrape_content
from bookmarks.lib.nlp import KeyWordExtractor

from ._base import BaseTagger, Tag

class IntelligentTagger(BaseTagger):


    def __init__(self, model: Any | None = None):
        super().__init__("AI")
        if model is None:
            self.model = KeyWordExtractor()
        else:
            self.model = model
    

    def extract(self, url: str, content: str | None = None) -> List[Tag]:

        if content is not None: # extract keywords directly 
            pass
            
        text = scrape_content(url)
        results = self.model.extract_keywords(text)[0]
        print("---------printing results of keywords extraction ------------------------")
        print(results)
        return [ self._to_tag(tag) for (tag, score) in results]
        

    def get_tags(self, urls: List[str], contents: List[str] | None = None) -> List[Tag]:
        return super().get_tags(urls, contents)
    
