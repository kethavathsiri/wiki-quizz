"""
Wikipedia scraper module for extracting article content
Improved approach: Extract only the main article text and paragraphs
"""
import requests
import re
from bs4 import BeautifulSoup, NavigableString
from typing import Dict, List, Tuple
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)

def validate_wikipedia_url(url: str) -> bool:
    """Validate if URL is a valid Wikipedia article URL"""
    try:
        parsed = urlparse(url)
        return "wikipedia.org" in parsed.netloc and "/wiki/" in parsed.path
    except Exception as e:
        logger.error(f"URL validation error: {e}")
        return False

def fetch_article(url: str) -> Tuple[str, str]:
    """
    Fetch Wikipedia article content
    Returns: (html_content, article_title)
    """
    if not validate_wikipedia_url(url):
        raise ValueError(f"Invalid Wikipedia URL: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text, ""
    except requests.RequestException as e:
        logger.error(f"Failed to fetch URL {url}: {e}")
        raise

def extract_title(soup: BeautifulSoup) -> str:
    """Extract article title from Wikipedia page"""
    try:
        title_element = soup.find("h1", class_="firstHeading")
        if title_element:
            return title_element.get_text(strip=True)
        return "Unknown"
    except Exception as e:
        logger.error(f"Error extracting title: {e}")
        return "Unknown"

def clean_text(text: str) -> str:
    """Clean text by removing noise while preserving structure"""
    # First, handle Unicode characters that can appear in Wikipedia text
    text = text.replace('\u00a0', ' ')  # Non-breaking space
    text = text.replace('\u2013', '-')  # En-dash
    text = text.replace('\u2014', '-')  # Em-dash
    text = text.replace('\u2019', "'")  # Right single quotation mark
    text = text.replace('\u201c', '"')  # Left double quotation mark
    text = text.replace('\u201d', '"')  # Right double quotation mark
    
    # Remove reference markers [1], [2], etc.
    text = re.sub(r'\[\d+\]', '', text)
    # Remove phonetic transcriptions /.../ 
    text = re.sub(r'/[^/]*/', '', text)
    # Remove [edit] markers
    text = re.sub(r'\[edit\]', '', text)
    # Remove HTML entity references
    text = re.sub(r'&[a-zA-Z]+;', '', text)
    # Add space before lowercase letter that follows uppercase (word splitting)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Remove special Unicode characters but keep common ones and em-dashes
    text = re.sub(r'[^\w\s\-.,;:!?()"\'–—°\n]', '', text, flags=re.UNICODE)
    # Normalize whitespace
    text = re.sub(r' +', ' ', text)
    # Remove spaces before common punctuation
    text = re.sub(r'\s+([,.;:!?)])', r'\1', text)
    # Add space after opening parenthesis and before closing
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)
    text = re.sub(r'\n\s*\n+', '\n', text)  # Remove excessive blank lines
    return text.strip()

def extract_summary(soup: BeautifulSoup) -> str:
    """Extract article summary (first paragraph) with better text handling"""
    try:
        content = soup.find("div", id="mw-content-text")
        if not content:
            return ""
        
        # Find first substantive paragraph (skip infoboxes, etc.)
        paragraphs = content.find_all("p", recursive=True)
        
        for p in paragraphs:
            # Skip if paragraph is too short
            text = p.get_text(separator=" ", strip=True)
            if len(text) < 100:
                continue
            
            # Check if paragraph is just metadata
            if any(word in text.lower() for word in ['wikipedia', 'disambiguation']):
                continue
            
            # Clean and return
            text = clean_text(text)
            return text[:600]
        
        return ""
    except Exception as e:
        logger.error(f"Error extracting summary: {e}")
        return ""

def extract_sections(soup: BeautifulSoup) -> List[str]:
    """Extract main section titles from article"""
    try:
        sections = []
        content = soup.find("div", id="mw-content-text")
        if not content:
            return sections
        
        # Find all h2 and h3 headings
        headings = content.find_all(["h2", "h3"])
        
        for heading in headings:
            # Get the heading text
            span = heading.find("span", class_="mw-headline")
            if span:
                text = span.get_text(strip=True)
                # Filter out common non-section headings
                if (text and 
                    text != "Contents" and 
                    len(text) < 100 and
                    not any(x in text.lower() for x in ['edit', 'references', 'notes'])):
                    sections.append(text)
        
        return sections[:15]
    except Exception as e:
        logger.error(f"Error extracting sections: {e}")
        return []

def extract_key_entities(soup: BeautifulSoup) -> Dict[str, List[str]]:
    """
    Extract key entities (people, organizations, locations) from infobox and bold text
    """
    try:
        entities = {
            "people": [],
            "organizations": [],
            "locations": []
        }
        
        # First try to extract from infobox
        infobox = soup.find("table", class_="infobox")
        if infobox:
            rows = infobox.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                if len(cells) >= 2:
                    label = cells[0].get_text(separator=" ", strip=True).lower()
                    value = cells[1].get_text(separator=" ", strip=True)
                    
                    if not value or len(value) > 80:
                        continue
                    
                    # Categorize based on label
                    if any(word in label for word in ["birth", "born", "name", "founder"]):
                        if value not in entities["people"]:
                            entities["people"].append(value)
                    elif any(word in label for word in ["organization", "company", "institution"]):
                        if value not in entities["organizations"]:
                            entities["organizations"].append(value)
                    elif any(word in label for word in ["place", "location", "country", "city"]):
                        if value not in entities["locations"]:
                            entities["locations"].append(value)
        
        # Fallback: Extract from bold text in first few paragraphs
        if not entities["people"]:
            content = soup.find("div", id="mw-content-text")
            if content:
                paragraphs = content.find_all("p", limit=5)
                for p in paragraphs:
                    bolds = p.find_all("b")
                    for bold in bolds:
                        text = bold.get_text(separator=" ", strip=True)
                        if 5 < len(text) < 50 and text not in entities["people"]:
                            # Basic check: looks like a name or entity
                            if not text.isdigit() and len(text.split()) <= 4:
                                entities["people"].append(text)
        
        # Limit to 5 of each type
        for key in entities:
            entities[key] = entities[key][:5]
        
        return entities
    except Exception as e:
        logger.error(f"Error extracting entities: {e}")
        return {"people": [], "organizations": [], "locations": []}

def extract_full_text(soup: BeautifulSoup) -> str:
    """
    Extract full article text for LLM processing
    Better approach: Extract paragraph by paragraph
    """
    try:
        content = soup.find("div", id="mw-content-text")
        if not content:
            return ""
        
        # Remove unwanted elements
        for element in content.find_all(["script", "style", "sup", "span"]):
            if element.name == "sup" or (element.name == "span" and element.get("class") == ["mw-editsection"]):
                element.decompose()
        
        paragraphs = []
        
        # Extract paragraphs while preserving structure
        for element in content.find_all(["p", "h2", "h3"]):
            if element.name == "p":
                text = element.get_text(separator=" ", strip=True)
                if len(text) > 20:  # Skip very short paragraphs
                    text = clean_text(text)
                    if text:
                        paragraphs.append(text)
            elif element.name in ["h2", "h3"]:
                span = element.find("span", class_="mw-headline")
                if span:
                    heading = span.get_text(strip=True)
                    if heading and heading != "Contents":
                        paragraphs.append(f"\n{heading}\n")
        
        # Join paragraphs with newlines
        full_text = "\n".join(paragraphs)
        
        return full_text[:8000]
    except Exception as e:
        logger.error(f"Error extracting full text: {e}")
        return ""

def scrape_wikipedia_article(url: str) -> Dict:
    """
    Main scraping function that orchestrates all extraction
    Returns dictionary with extracted article data
    """
    try:
        logger.info(f"Scraping: {url}")
        html_content, _ = fetch_article(url)
        soup = BeautifulSoup(html_content, "html.parser")
        
        title = extract_title(soup)
        summary = extract_summary(soup)
        sections = extract_sections(soup)
        key_entities = extract_key_entities(soup)
        full_text = extract_full_text(soup)
        
        logger.info(f"Extracted: {len(summary)} char summary, {len(sections)} sections, {len(full_text)} char full text")
        
        return {
            "url": url,
            "title": title,
            "summary": summary,
            "sections": sections,
            "key_entities": key_entities,
            "full_text": full_text,
            "raw_html": html_content
        }
    except Exception as e:
        logger.error(f"Error scraping article: {e}")
        raise
