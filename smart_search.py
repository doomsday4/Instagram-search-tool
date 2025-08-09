import json
import os
import pickle
import numpy as np
import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity

# --- Configuration ---
# 1. Paste the full path to your Instagram data folder.
ROOT_DIRECTORY = "/Users/.../.../instagram-...56-2025-08-03-9SQD9oCT" # PASTE YOUR FOLDER PATH HERE

# 2. Paste your Google AI API Key here.
API_KEY = "..." # PASTE YOUR API KEY HERE

# --- Constants ---
INDEX_FILE = 'instagram_data_index.pkl'
EMBEDDING_MODEL = 'models/embedding-001'

# --- Setup Google AI ---
try:
    genai.configure(api_key=API_KEY)
    print("Google AI Configured Successfully.")
except Exception as e:
    print(f"Error configuring Google AI. Please check your API_KEY. Error: {e}")

# --- Helper Functions ---
def load_json_data(file_path):
    full_path = os.path.join(ROOT_DIRECTORY, file_path)
    if not os.path.exists(full_path):
        return []
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def get_embedding(text):
    """Generates an embedding for a given piece of text."""
    if not text:
        return None
    try:
        # Corrected direct call to the embedding function
        return genai.embed_content(model=EMBEDDING_MODEL, content=text)['embedding']
    except Exception as e:
        print(f"Could not get embedding for text: '{text[:30]}...'. Error: {e}")
        return None

def create_and_save_index():
    """Processes all data, generates embeddings, and saves them to a file."""
    print("Creating a new search index. This may take a few minutes...")
    
    all_content = []

    # 1. Process Saved and Liked Posts
    for file_path, data_key in [
        ("your_instagram_activity/saved/saved_posts.json", "saved_saved_media"),
        ("your_instagram_activity/likes/liked_posts.json", "likes_media_likes")
    ]:
        data = load_json_data(file_path)
        post_list = data.get(data_key, [])
        for item in post_list:
            try:
                author = item.get('title', '')
                caption_data = item.get('string_list_data', [{}])[0]
                caption = caption_data.get('value', '')
                link = caption_data.get('href', '#')
                full_text = f"{author}: {caption}"
                if full_text.strip():
                    all_content.append({'text': full_text, 'link': link, 'source': 'Post'})
            except (IndexError, AttributeError):
                continue
    
    # 2. Process Ads Data
    for file_path in [
        "ads_information/ads_and_topics/ads_viewed.json",
        "ads_information/ads_and_topics/ads_clicked.json"
    ]:
        data = load_json_data(file_path)
        for ad in data:
            text = ''
            if isinstance(ad, dict):
                text = f"Ad by {ad.get('author', '')}: {ad.get('title', '')}"
            elif isinstance(ad, str):
                text = f"Ad Topic: {ad}"
            if text.strip():
                all_content.append({'text': text, 'link': 'N/A', 'source': 'Ad'})

    # 3. Generate embeddings for all content
    indexed_data = []
    for i, content in enumerate(all_content):
        print(f"Indexing item {i+1}/{len(all_content)}...")
        embedding = get_embedding(content['text'])
        if embedding:
            content['embedding'] = embedding
            indexed_data.append(content)
            
    # 4. Save the index to a file
    with open(INDEX_FILE, 'wb') as f:
        pickle.dump(indexed_data, f)
        
    print(f"\nIndex with {len(indexed_data)} items has been created and saved as '{INDEX_FILE}'")
    return indexed_data

def search_with_llm(query, indexed_data, top_k=5):
    """Performs semantic search using embeddings."""
    print(f"Generating embedding for your query: '{query}'")
    query_embedding = get_embedding(query)
    
    if not query_embedding:
        print("Could not process your query.")
        return
        
    content_embeddings = np.array([item['embedding'] for item in indexed_data])
    similarities = cosine_similarity([query_embedding], content_embeddings)[0]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    print("\n--- Top Search Results ---")
    for i in top_indices:
        item = indexed_data[i]
        similarity_score = similarities[i]
        print(f"\nRelevance Score: {similarity_score:.4f}")
        print(f"Source: {item['source']}")
        print(f"Content: {item['text'][:250]}...")
        if item['link'] != 'N/A':
            print(f"Link: {item['link']}")

# --- Main Program ---
if __name__ == "__main__":
    if not ROOT_DIRECTORY or not API_KEY:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! ERROR: Please set the ROOT_DIRECTORY and API_KEY at the top of the script !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        if os.path.exists(INDEX_FILE):
            print(f"Loading existing search index from '{INDEX_FILE}'...")
            with open(INDEX_FILE, 'rb') as f:
                indexed_data = pickle.load(f)
            print("Index loaded.")
        else:
            indexed_data = create_and_save_index()

        while True:
            query = input("\nEnter your search query (or type 'quit' to exit): ")
            if query.lower() == 'quit':
                break
            search_with_llm(query, indexed_data)