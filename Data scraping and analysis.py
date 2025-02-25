import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Function to scrape book data
def scrape_books(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    books = []
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text[1:]  # Remove the £ symbol
        rating = book.p['class'][1]  # Get the rating (e.g., "Three")
        books.append({
            'Title': title,
            'Price': float(price),  # Convert price to float
            'Rating': rating
        })
    return books

# Scrape multiple pages
all_books = []
base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
for page in range(1, 6):  # Scrape first 5 pages
    url = base_url.format(page)
    all_books.extend(scrape_books(url))

# Convert to a DataFrame
df = pd.DataFrame(all_books)

# Clean the data
rating_map = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}
df['Rating'] = df['Rating'].map(rating_map)

# Check for missing values
print(df.isnull().sum())

# Drop duplicates (if any)
df.drop_duplicates(inplace=True)

# Summary statistics
print(df.describe())

# Plot the distribution of prices
plt.figure(figsize=(10, 6))
plt.hist(df['Price'], bins=20, color='blue', edgecolor='black')
plt.title('Distribution of Book Prices')
plt.xlabel('Price (£)')
plt.ylabel('Frequency')
plt.show()

# Group by rating and calculate average price
avg_price_by_rating = df.groupby('Rating')['Price'].mean()

# Plot the average price by rating
plt.figure(figsize=(10, 6))
avg_price_by_rating.plot(kind='bar', color='green')
plt.title('Average Book Price by Rating')
plt.xlabel('Rating')
plt.ylabel('Average Price (£)')
plt.xticks(rotation=0)
plt.show()

# Sort by price and get the top 10 most expensive books
top_10_expensive = df.nlargest(10, 'Price')

# Plot the top 10 most expensive books
plt.figure(figsize=(10, 6))
plt.barh(top_10_expensive['Title'], top_10_expensive['Price'], color='purple')
plt.title('Top 10 Most Expensive Books')
plt.xlabel('Price (£)')
plt.ylabel('Book Title')
plt.gca().invert_yaxis()  # Invert y-axis to show the highest at the top
plt.show()

# Save the cleaned data
df.to_csv('books_data.csv', index=False)