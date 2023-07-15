from typing import List, Optional, Any

from bookmarks.lib.web_scraper import scrape_content
from bookmarks.lib.nlp import KeyWordExtractor, tokenize_into_paragraphs, tokenize_into_sentences

from ._base import BaseTagger, Tag

class IntelligentTagger(BaseTagger):


    def __init__(self, model: Any | None = None):
        super().__init__("AI")
        if model is None:
            self.model = KeyWordExtractor()
        else:
            self.model = model
    

    def extract(self, url: str, tokenize: bool = False, content: str | None = None) -> List[Tag]:

        if content is not None: # extract keywords directly 
            pass

        docs = scrape_content(url)
        if tokenize:
            docs = tokenize_into_sentences(docs)

        results = self.model.extract_keywords(docs)[0]
        return [ self._to_tag(tag) for (tag, _) in results]
        

    def get_tags(self, urls: List[str], contents: List[str] | None = None) -> List[Tag]:
        return super().get_tags(urls, contents)
    
