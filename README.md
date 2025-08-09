Instagram Personal Search Engine
================================

This project empowers you to create a powerful, private, and local search engine for your personal Instagram activity. Have you ever struggled to find a post you know you saved, liked, or saw in an ad? This tool solves that problem by allowing you to search through your entire Instagram data export using either basic keywords or advanced, AI-powered semantic search.

The Problem
-----------

Instagram is a treasure trove of personal inspiration, saved recipes, liked art, and interesting ads. However, finding this content later is incredibly difficult. The native search is limited, and collections can become cluttered. This tool gives you the power to instantly find what you're looking for by searching the captions, usernames, and ad data of content you've interacted with.

Features
--------

*   **100% Private:** All your data is processed locally on your machine. Nothing is ever uploaded to a third-party service.
    
*   **Two Search Modes:**
    
    1.  **Basic Keyword Search (main.py):** A fast, simple script that finds exact keyword matches in your data.
        
    2.  **Smart Semantic Search (smart\_search.py):** Uses Google's AI models to understand the _meaning_ of your query. Find "room decor" posts even if they don't contain that exact phrase!
        
*   **Comprehensive Data:** Searches through your liked posts, saved posts, and ad history.
    
*   **Easy to Use:** Simple command-line interface.
    

How It Works
------------

The tool works by parsing the JSON files from your official Instagram data export.

1.  **Basic Search** simply iterates through the text in these files to find exact keyword matches.
    
2.  **Smart Search** takes this a step further. It performs a one-time "indexing" process where it converts the text of every post and ad into a numerical representation called a **vector embedding** using a Google AI model. When you search, it converts your query into an embedding and then finds the most mathematically similar (and therefore contextually relevant) items from your data.
    

Setup and Installation
----------------------

Follow these steps to get the search engine running.

### 1\. Prerequisites

*   **Python 3.x:** Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
    

### 2\. Clone the Repository

Clone this repository to your local machine:

```
git clone cd
```

### 3\. Install Dependencies

Install the required Python libraries for the smart search script. The basic script requires no extra libraries.

```
pip install google-generativeai numpy scikit-learn
```

### 4\. Get Your Instagram Data

This is the most crucial step. You need to request a download of your data from Instagram.

1.  Go to your Instagram **Profile** > **Settings and privacy** > **Accounts Center**.
    
2.  Navigate to **Your information and permissions** > **Download your information**.
    
3.  Click **Request a download**, select your profile, and choose the types of information. Ensure **Likes**, **Saved**, and **Ads** and **businesses** are selected.
    
4.  **CRITICAL:** For the Format, you must select **JSON**.
    
5.  Submit the request. It can take a few hours or days for Instagram to prepare your data. You will receive an email when it's ready.
    
6.  Download the .zip file, and **unzip it**.
    

### 5\. Get Your Google AI API Key (For Smart Search Only)

1.  Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
    
2.  Click **"Create** API key" and copy the key it generates. You will need this for the smart\_search.py script.
    

Usage
-----

Before running either script, you must configure the ROOT\_DIRECTORY variable at the top of the file.

1.  Find the unzipped Instagram data folder on your computer.
    
2.  **Copy the full path** to this folder.
    
3.  Open either main.py or smart\_search.py and paste the path into the ROOT\_DIRECTORY = "" variable.
    

### Script 1: Basic Keyword Search (main.py)

This script is fast and simple. It looks for exact word matches.

**To Run:**

```
python main.py
```

The script will load your data and then prompt you for a keyword.

**Example:**

```
Enter a keyword to search (or type 'quit' to exit): design 
--- Searching for 'design' ---  
>>> Searching in SAVED posts...  
Found Post by: awesome.designs    
Caption: Check out this awesome minimalist chair design...    
Link: ...
```

### Script 2: Smart Semantic Search (smart\_search.py)

This script understands the context and meaning of your search. It's perfect for when you don't remember the exact keywords.

**Configuration:** Before running, you must fill in **both** the ROOT\_DIRECTORY and your API\_KEY at the top of the smart\_search.py file.

**To Run:**

```
python smart_search.py
```

**First-Time Indexing:** The very first time you run this script, it will need to create a search index. This involves sending your text data (locally) to the Google AI API to generate embeddings. This process can take several minutes depending on the size of your Instagram data. It will create a file named instagram\_data\_index.pkl. All subsequent runs will be fast as they will load directly from this file.

**Example:**

```
Enter your search query (or type 'quit' to exit): cozy ideas for my bedroom  
--- Top Search Results ---  
Relevance Score: 0.8123  
Source: Post  
Content: hyggehome: Loving this warm lighting and the soft textures in this space. It makes everything feel so inviting and comfortable. 
#interiordesign #bedroomgoals...  
Link: ...  
Relevance Score: 0.7985  
Source: Post  
Content: diy.decor: A simple DIY for creating a beautiful wall hanging that adds a personal touch to any room!  
Link: ...
```

Disclaimer
----------

This project is for personal use only. All of your Instagram data is processed and stored locally on your machine. No personal data is tracked or uploaded by these scripts.