from docx import Document

def load_fest_documents(doc_path: str):
    """
    Load DOCX with memory efficiency.
    """
    try:
        doc = Document(doc_path)
        sections = []
        buffer = []
        max_sections = 20  # Limit sections

        for para in doc.paragraphs:
            if len(sections) >= max_sections:
                break
                
            text = para.text.strip()
            if not text:
                continue

            # Chunk on headings
            if text.isupper() or text.endswith(":"):
                if buffer:
                    sections.append(" ".join(buffer)[:500])  # Truncate
                    buffer = []

            buffer.append(text)

        if buffer and len(sections) < max_sections:
            sections.append(" ".join(buffer)[:500])

        return sections
        
    except Exception as e:
        print(f"❌ Error loading document: {e}")
        return []
