import os
import json
import re
import yaml
from collections import defaultdict

DOCS_DIR = os.getenv("DOCS_DIR", "docs")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "site/faq.json")

def parse_markdown(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return None

    # Extract frontmatter
    frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not frontmatter_match:
        return None

    try:
        metadata = yaml.safe_load(frontmatter_match.group(1))
    except yaml.YAMLError:
        return None

    if "faq_category" not in metadata:
        return None

    category = metadata["faq_category"]
    faq_items = []

    # Regex to find questions (H2 or H3 headers followed by answer text)
    # Assumes format:
    # ## Question?
    # Answer...
    
    # Split by headers (assuming H2 or H3 start questions)
    sections = re.split(r'\n(#{2,3}) ', content)
    
    # Process sections (skip first which is "Introduction")
    for i in range(1, len(sections), 2):
        header_level = sections[i]
        section_content = sections[i+1]
        
        # Extract title (first line)
        lines = section_content.strip().split('\n')
        if not lines:
            continue
            
        question = lines[0].strip()
        answer = '\n'.join(lines[1:]).strip()
        
        # Simple heuristic: if it looks like a question or marked as FAQ
        if "?" in question or "FAQ" in question:
             faq_items.append({
                "question": question,
                "answer": answer
            })

    return category, faq_items

def main():
    faq_data = {
        "templates": [],
        "billing": [],
        "general": []
    }
    
    # Map relative_path -> { lang: full_path }
    file_groups = defaultdict(dict)

    print(f"Scanning {DOCS_DIR}...")

    # Walk through docs
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                
                # Determine relative path and language
                rel_path = os.path.relpath(file_path, DOCS_DIR)
                
                lang = "en"
                canonical_rel_path = rel_path
                
                # Check if it's a localized file (e.g., inside "uk/" folder)
                # We assume top-level folders in docs/ might be languages if they match our targets
                path_parts = rel_path.split(os.sep)
                if len(path_parts) > 1 and path_parts[0] in ["uk", "ru", "es"]: # Add other languages as needed
                    lang = "ua" if path_parts[0] == "uk" else path_parts[0]
                    canonical_rel_path = os.path.join(*path_parts[1:])
                
                file_groups[canonical_rel_path][lang] = file_path

    # Process grouped files
    for rel_path, localizations in file_groups.items():
        # We need at least one file to proceed. 
        # We'll try to find a category from any of them.
        category = None
        merged_items = []
        
        # First pass: Parse all languages
        parsed_docs = {}
        max_items = 0
        
        for lang, path in localizations.items():
            result = parse_markdown(path)
            if result:
                cat, items = result
                parsed_docs[lang] = items
                if not category:
                    category = cat
                # Simple validation: if categories mismatch across languages for the same file, 
                # we stick to the first one found or maybe warn? 
                # For now, assume consistency.
                max_items = max(max_items, len(items))
        
        if category and category in faq_data:
            # Merge items by index
            for i in range(max_items):
                merged_item = {
                    "question": {},
                    "answer": {}
                }
                
                for lang, items in parsed_docs.items():
                    if i < len(items):
                        merged_item["question"][lang] = items[i]["question"]
                        merged_item["answer"][lang] = items[i]["answer"]
                
                # Only add if we have at least one language content (should be true if max_items > 0)
                if merged_item["question"]:
                    faq_data[category].append(merged_item)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(faq_data, f, ensure_ascii=False, indent=2)

    print(f"Generated {OUTPUT_FILE} with {sum(len(v) for v in faq_data.values())} items")

if __name__ == "__main__":
    main()
