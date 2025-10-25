import fitz  # PyMuPDF
import os
import re


def extract_text_from_file(path: str) -> str:
    """
    Extract text from a .pdf or .txt file path. Returns a single string.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    else:
        return ""


def extract_text_from_pdf(path: str) -> str:
    """
    Use PyMuPDF (fitz) to extract text from each page.
    """
    text_parts = []
    try:
        doc = fitz.open(path)
        for page in doc:
            text = page.get_text("text")
            if text:
                text_parts.append(text)
        doc.close()
    except Exception:
        return ""

    return "\n".join(text_parts)


def clean_text(text: str) -> str:
    """
    Basic cleaning to remove repeated headers/footers and fix line breaks.
    This is heuristic-based and intentionally conservative.
    """
    if not text:
        return ""

    # Normalize line endings
    t = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove multiple consecutive short lines that look like page numbers or headers
    lines = [ln.strip() for ln in t.split("\n")]

    cleaned_lines = []
    for ln in lines:
        # drop pure page-number lines
        if re.fullmatch(r"\d{1,4}", ln):
            continue
        # drop header/footer like 'Chapter 1' repeated very frequently heuristic: very short and alphanumeric
        if len(ln) <= 3 and re.match(r"^[A-Za-z0-9]{1,3}$", ln):
            continue
        cleaned_lines.append(ln)

    # Join lines but preserve paragraph breaks: if a line ends with a hyphen, join without space
    out_parts = []
    for ln in cleaned_lines:
        if not out_parts:
            out_parts.append(ln)
            continue
        prev = out_parts[-1]
        if prev.endswith("-"):
            out_parts[-1] = prev[:-1] + ln
        elif ln == "":
            out_parts.append(ln)
        elif ln and ln[0].islower():
            # continuation line — join with space
            out_parts[-1] = prev + " " + ln
        else:
            out_parts.append(ln)

    cleaned = "\n\n".join([p for p in out_parts if p.strip() != ""])

    # Collapse multiple spaces
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    return cleaned.strip()


def summarize_text(text: str, max_chars: int = 2000) -> str:
    """
    Lightweight summarizer stub: returns the first N characters or first few sentences.
    Replace this with a call to an LLM summarization endpoint later (OpenAI/Gemini/etc.).
    """
    if not text:
        return ""

    # Try to return first 3 sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)
    summary = " ".join(sentences[:3])
    if len(summary) > max_chars:
        return summary[:max_chars].rsplit(" ", 1)[0] + "..."
    return summary
