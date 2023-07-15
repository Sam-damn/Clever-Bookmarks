def preprocess_text(text):
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
