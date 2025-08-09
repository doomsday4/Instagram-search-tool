import json
import os

# --- Configuration ---
# IMPORTANT: Before you run, paste the full path to your unzipped Instagram data folder here.
ROOT_DIRECTORY = "/Users/.../.../instagram-...56-2025-08-03-9SQD9oCT" # PASTE YOUR FOLDER PATH HERE

def load_json_data(file_path):
    """Safely loads a JSON file if it exists."""
    full_path = os.path.join(ROOT_DIRECTORY, file_path)
    if not os.path.exists(full_path):
        print(f"Warning: File not found at {full_path}")
        return []
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {full_path}: {e}")
        return []

# --- Search Functions ---
def search_posts(data, keyword):
    """Searches through liked or saved posts."""
    results = []
    # Determine if the data is from 'likes' or 'saved'
    post_list = data.get('likes_media_likes', []) if 'likes_media_likes' in data else data.get('saved_saved_media', [])
    for item in post_list:
        try:
            caption_data = item.get('string_list_data', [{}])[0]
            caption_text = caption_data.get('value', '').lower()
            author = item.get('title', '').lower()
            
            if keyword in caption_text or keyword in author:
                link = caption_data.get('href', '#')
                print(f"\nFound Post by: {item.get('title', 'N/A')}")
                print(f"  Caption: {caption_text[:150]}...")
                print(f"  Link: {link}")
                results.append(item)
        except (IndexError, AttributeError):
            # Skip this item if it doesn't have the expected structure
            continue
    return results

def search_ads(data, keyword):
    """Searches through ads data, handling different formats."""
    results = []
    # Some ad files are lists of strings, others are lists of dicts
    ad_list = data.get('ads_interests_ad_topics', []) if isinstance(data, dict) else data
    for ad in ad_list:
        found = False
        # Handle if the 'ad' is a dictionary (like in ads_clicked.json)
        if isinstance(ad, dict):
            author = ad.get('author', '').lower()
            title = ad.get('title', '').lower()
            if keyword in author or keyword in title:
                print(f"\nFound Ad:")
                print(f"  Advertiser: {ad.get('author', 'N/A')}")
                print(f"  Title: {ad.get('title', 'N/A')}")
                found = True
        # Handle if the 'ad' is just a string (like in ads_viewed.json)
        elif isinstance(ad, str):
            if keyword in ad.lower():
                print(f"\nFound Viewed Ad Topic: {ad}")
                found = True
        
        if found:
            results.append(ad)
    return results
    

# --- Main Program ---
if __name__ == "__main__":
    if not ROOT_DIRECTORY:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! ERROR: Please set the ROOT_DIRECTORY in the script !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        # Load all the relevant data
        print("Loading your Instagram data...")
        liked_posts = load_json_data("your_instagram_activity/likes/liked_posts.json")
        saved_posts = load_json_data("your_instagram_activity/saved/saved_posts.json")
        ads_viewed = load_json_data("ads_information/ads_and_topics/ads_viewed.json")
        ads_clicked = load_json_data("ads_information/ads_and_topics/ads_clicked.json")
        print("Data loaded successfully!")

        # Search loop
        while True:
            keyword = input("\nEnter a keyword to search (or type 'quit' to exit): ").lower()
            if keyword == 'quit':
                break
            
            print(f"\n--- Searching for '{keyword}' ---")
            
            print("\n>>> Searching in SAVED posts...")
            search_posts(saved_posts, keyword)
            
            print("\n>>> Searching in LIKED posts...")
            search_posts(liked_posts, keyword)
            
            print("\n>>> Searching in VIEWED ads...")
            search_ads(ads_viewed, keyword)

            print("\n>>> Searching in CLICKED ads...")
            search_ads(ads_clicked, keyword)

            print("\n--- Search complete ---")