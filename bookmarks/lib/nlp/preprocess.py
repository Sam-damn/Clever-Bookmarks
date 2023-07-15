import nltk
nltk.download('punkt')

def tokenize_into_paragraphs(text):
    # Split text into lines
    lines = text.splitlines()
    
    # Group lines into paragraphs
    paragraphs = []
    current_paragraph = []
    
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if line:
            current_paragraph.append(line)
        elif current_paragraph:
            paragraphs.append(" ".join(current_paragraph))
            current_paragraph = []
    
    # Handle the last paragraph if not followed by an empty line
    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))
    
    return paragraphs
def tokenize_into_sentences(text):
    sentences = nltk.sent_tokenize(text)
    combined_sentences = []
    for i,_ in enumerate(sentences):
        if i % 3 == 0 and i+2 < len(sentences):
            combined_sentences.append(' '.join([sentences[i], sentences[i+1], sentences[i+2]]))

    return combined_sentences
