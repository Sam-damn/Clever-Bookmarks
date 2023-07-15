from bookmarks.tags.IntelligentTagger import IntelligentTagger


tagger = IntelligentTagger()
values = tagger.extract("https://dev.to/jankrepl/mltype-typing-practice-for-programmers-1d4f")
print(values)