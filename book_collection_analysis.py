#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import csv
import time

def fetch_openlibrary_data(query, page):
    """
    Fetch data from the Open Library search API for a specific query and page.
    """
    url = f"https://openlibrary.org/search.json?q={query}&page={page}"
    print(f"Fetching data from URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for query: {query}, page: {page}. Status code: {response.status_code}")
        return None

def get_books_data(queries, max_pages):
    """
    Fetch books data for a list of queries across multiple pages.
    """
    books = []
    for query in queries:
        for page in range(1, max_pages + 1):
            print(f"Fetching data for query: '{query}', page: {page}...")
            data = fetch_openlibrary_data(query, page)
            if data and 'docs' in data:
                for book in data['docs']:
                    books.append({
                        "title": book.get("title", "N/A"),
                        "author_name": ", ".join(book.get("author_name", ["N/A"])),
                        "first_publish_year": book.get("first_publish_year", "N/A"),
                        "isbn": ", ".join(book.get("isbn", ["N/A"])),
                        "publish_date": ", ".join(book.get("publish_date", ["N/A"])),
                        "subject": ", ".join(book.get("subject", ["N/A"])),
                        "publisher": ", ".join(book.get("publisher", ["N/A"])),
                        "language": ", ".join(book.get("language", ["N/A"]))
                    })
            else:
                break
            time.sleep(1)  # Respect API rate limits
    return books

def save_books_to_csv(filename, books):
    """
    Save the collected books data into a CSV file.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["title", "author_name", "first_publish_year", "isbn", "publish_date", "subject", "publisher", "language"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for book in books:
            writer.writerow(book)

if __name__ == "__main__":
    print("Collecting book data from Open Library API...")
    queries = [
        "lord","harry","science","game","lord+of+the+rings", "harry+potter", "game+of+thrones", "science+fiction", "fantasy", "history", "biography", "romance", "mystery", "thriller", "adventure", "children+books", "self+help", "non+fiction", "classic+novels", "poetry", "drama", "horror", "graphic+novels", "philosophy", "psychology", "education", "health", "wellness", "art", "business", "technology", "travel", "cooking", "sports", "politics", "religion", "culture", "memoir", "science", "nature", "environment", "astronomy", "mathematics", "fiction", "literature", "writing", "short+stories", "young+adult", "middle+grade", "anthology", "true+crime", "historical+fiction", "war", "music", "media", "architecture", "design", "engineering", "economics", "sociology", "anthropology", "linguistics", "encyclopedia", "dictionary", "mythology", "folklore", "fairy+tales", "comedy", "satire", "political+science", "cultural+studies", "gender+studies", "spirituality", "ancient+history", "renaissance", "modern+history", "biological+sciences", "physics", "chemistry", "earth+sciences", "space+exploration", "dystopian", "utopian", "cyberpunk", "steampunk", "paranormal", "supernatural", "western", "crime+fiction", "detective+fiction", "medical+science", "veterinary+science", "genetics", "evolution", "botany", "zoology", "marine+biology", "urban+fantasy",
"space+opera","military+history","psychological+thriller","post-apocalyptic"    ]
    max_pages = 10

    books_data = get_books_data(queries, max_pages)
    print(f"Collected {len(books_data)} records.")

    save_books_to_csv("openlibrary_books.csv", books_data)
    print("Data saved successfully to openlibrary_books.csv.")


# In[32]:


get_ipython().system('pip install pymongo')


# In[33]:


from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Establish a connection to MongoDB
client = MongoClient("mongodb+srv://ram:TLzsC0e2BNePL8wp@cluster0.bs2nf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["books"]
collection = db["books"]


# # Load your dataset
df = pd.read_csv("openlibrary_books.csv")

# Convert the dataframe to a list of dictionaries
data = df.to_dict(orient="records")

# Insert data into MongoDB
collection.insert_many(data)


# In[34]:


# Step 1: Load data from MongoDB into pandas DataFrame
mongo_data = collection.find()  # Fetch all data from MongoDB
df = pd.DataFrame(list(mongo_data))  # Convert to DataFrame

# Check the number of rows and columns in the database
row_count = collection.count_documents({})
print(f"Number of rows in MongoDB: {row_count}")
print(f"Columns in dataset: {df.columns.tolist()}")


# In[35]:


# Step 2: Data Cleaning (Silver Layer)
# Remove rows with missing values
df_cleaned = df.dropna()

# Remove duplicate rows
df_cleaned = df_cleaned.drop_duplicates()

# Standardize column names
df_cleaned.columns = [col.lower().replace(" ", "_") for col in df_cleaned.columns]

# Check the cleaned dataset
print("\nCleaned Data Sample:")
print(df_cleaned.head())


# In[36]:


# Convert language column to lists
df["language"] = df["language"].str.split(", ")

# Aggregation 1: Count of books per author
books_per_author = df.groupby("author_name")["_id"].count().reset_index()
books_per_author.columns = ["author_name", "book_count"]

# Aggregation 2: Average first_publish_year per language
# Exploding the 'language' column to create a row for each language
df_exploded = df.explode("language")
average_publish_year = df_exploded.groupby("language")["first_publish_year"].mean().reset_index()

# Convert 'first_publish_year' to numeric, handling errors
df['first_publish_year'] = pd.to_numeric(df['first_publish_year'], errors='coerce')

# Fill NaN values with 0 and then calculate the decade
df["publish_decade"] = (df["first_publish_year"].fillna(0) // 10 * 10).astype(int)

books_by_decade = df.groupby("publish_decade")["_id"].count().reset_index()
books_by_decade.columns = ["publish_decade", "book_count"]


# In[37]:


# Horizontal Bar Chart: Top 10 authors with the most books
top_authors = books_per_author.nlargest(10, "book_count")
plt.figure(figsize=(10, 6))
plt.barh(top_authors["author_name"], top_authors["book_count"], color="teal")
plt.title("Top 10 Authors with the Most Books")
plt.xlabel("Number of Books")
plt.ylabel("Author")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("top_authors_bar_chart.png")
plt.show()


# In[38]:


# Top 5 Authors' Publication Trends Over Decades
top_5_authors = books_per_author.nlargest(5, "book_count")["author_name"].tolist()

# Filter df (which contains 'publish_decade') instead of df_exploded
top_authors_data = df[df["author_name"].isin(top_5_authors)]

# Explode 'language' column after filtering for top authors
top_authors_data = top_authors_data.explode("language")

author_trends = top_authors_data.groupby(["publish_decade", "author_name"])["_id"].count().unstack()

author_trends.plot(kind="line", figsize=(12, 6), marker="o")
plt.title("Top 5 Authors' Publication Trends Over Decades")
plt.xlabel("Decade")
plt.ylabel("Number of Books")
plt.legend(title="Author")
plt.tight_layout()
plt.savefig("author_trends_line_chart.png")
plt.show()


# In[39]:


# Donut Chart: Top 5 Languages by Book Count
language_counts = df_exploded["language"].value_counts()
top_languages = language_counts.head(5)

plt.figure(figsize=(8, 8))
plt.pie(
    top_languages,
    labels=top_languages.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=plt.cm.Paired.colors,
    wedgeprops=dict(width=0.4)
)
plt.title("Top 5 Languages by Book Count")
plt.savefig("top_languages_donut_chart.png")
plt.show()


# In[ ]:





# In[ ]:




