import os
import json
import re
import yaml

DOCS_DIR = "docs"
OUTPUT_FILE = "site/faq.json"

def parse_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

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

    # Walk through docs
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                result = parse_markdown(file_path)
                
                if result:
                    category, items = result
                    if category in faq_data:
                        # Transform to required format: { "question": { "en": "...", "ua": "..." }, "answer": ... }
                        # Currently we only parse the file, so we assume EN for now unless we detect language structure
                        # For simplicity, let's treat current file content as the "en" version if not specified otherwise
                        
                        # Check language path
                        lang = "en"
                        if "/uk/" in file_path:
                            lang = "ua"
                        
                        # This part is tricky because we need to merge translations if they are in separate files
                        # For MVP, let's just create separate entries or assume standard structure
                        
                        for item in items:
                            normalized_item = {
                                "question": { lang: item["question"] },
                                "answer": { lang: item["answer"] }
                            }
                            faq_data[category].append(normalized_item)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(faq_data, f, ensure_ascii=False, indent=2)

    print(f"Generated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
