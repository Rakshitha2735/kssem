import requests
from bs4 import BeautifulSoup
import re
import json

# Step 1: Define KSSEM Website URL
url = "https://kssem.edu.in"

# Step 2: Set headers to avoid bot detection
headers = {"User-Agent": "Mozilla/5.0"}

# Step 3: Fetch the webpage
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Step 4: Define key sections to extract
    relevant_sections = [
        "admission", "courses", "eligibility", "placement", "facilities",
        "principal", "teaching staff", "faculty", "fee structure", "course level",
        "contact", "email", "management", "phone", "about", "scholarship",
        "hostel", "campus", "events", "news", "announcements", "social media",
        "departments", "syllabus", "research", "accreditation", "clubs", "sports",
        "library", "laboratories", "ranking", "press release", "student life"
    ]

    extracted_data = {}

    # Step 5: Extract and categorize content
    for tag in soup.find_all(["h1", "h2", "h3", "p", "li", "span"]):
        text = tag.get_text(strip=True)

        for section in relevant_sections:
            if section in text.lower():
                if section not in extracted_data:
                    extracted_data[section] = []  # Create a category for each topic
                extracted_data[section].append(text)

    # Step 6: Extract Contact Details (Phone & Email)
    contact_details = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        if "tel:" in href or "mailto:" in href:
            contact_details.append(href.replace("tel:", "").replace("mailto:", ""))

    if contact_details:
        extracted_data["contact_details"] = contact_details

    # Step 7: Extract Social Media Links
    social_media_links = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        if any(platform in href for platform in ["facebook.com", "instagram.com", "linkedin.com", "youtube.com"]):
            social_media_links.append(href)

    if social_media_links:
        extracted_data["social_media"] = social_media_links

    # Step 8: Extract Events & News
    events = []
    for tag in soup.find_all(["h2", "h3", "p", "li"]):
        text = tag.get_text(strip=True)
        if any(keyword in text.lower() for keyword in ["event", "webinar", "workshop", "drive", "announcement"]):
            events.append(text)

    if events:
        extracted_data["events"] = events

    # Step 9: Extract Image URLs (Campus, Labs, Events)
    image_urls = []
    for img_tag in soup.find_all("img", src=True):
        img_url = img_tag["src"]
        if img_url.startswith("http"):  # Only absolute URLs
            image_urls.append(img_url)

    if image_urls:
        extracted_data["photos"] = image_urls

    # Step 10: Format extracted text for chatbot training
    formatted_text = ""
    for category, texts in extracted_data.items():
        formatted_text += f"\n\n### {category.upper()} ###\n"
        formatted_text += "\n".join(texts)

    # Step 11: Save structured text data
    with open("scraped_data.txt", "w", encoding="utf-8") as file:
        file.write(formatted_text)

    # Step 12: Save structured JSON data
    with open("scraped_data.json", "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, indent=4)

    print("✅ Successfully extracted **all KSSEM details** for chatbot!")

else:
    print(f"❌ Failed to retrieve data. Status Code: {response.status_code}")
