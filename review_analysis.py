from googlesearch import search
from collections import defaultdict
import urllib.request
from bs4 import BeautifulSoup
import re
from afinn import Afinn
import pandas as pd

movie = input("Enter movie name: ")
query = movie + " User review"
print(query)

r = " "  # Initializes an empty string
for j in search(query, num=40, stop=2,
                pause=2):  # Performs a Google search for the query with the top-level domain .co.in, retrieves up to 40 results, stops after 2 results, and pauses for 2 seconds between requests
    print(j)  # Prints each URL found in the search results
    r = j  # Stores the last URL found in the variable

response = urllib.request.urlopen(r)  # Opens the URL stored in r and retrieves the response
html = response.read()  # Reads the HTML content from the response
soup = BeautifulSoup(html, 'html.parser')  # Parses the HTML content using BeautifulSoup.

text = soup.get_text()  # Extracts all the text from the parsed HTML.
print(text)  # Prints the extracted text


def get_imdb_reviews(text1):  # Defines a function get_imdb_reviews to extract reviews from the HTML content.
    reviews = []
    for review_div in soup.find_all('div',
                                    class_="text show-more__control"):  # Finds all div elements with the class text show-more_control (specific to IMDb review structure)
        reviews.append(review_div.get_text())  # Appends the text of each found div to the reviews list.
    return reviews  # Returns the list of reviews


reviews = get_imdb_reviews(movie)  # Calls the get_imdb_reviews function and stores the returned reviews in reviews.

df = pd.DataFrame({'Review': reviews})  # Creates a DataFrame df with the reviews.
df


def cleanTxt(text):
    text = re.sub('@[A-Za-z0-9]+', '', text)  # Removes Twitter handles.
    text = re.sub('#', '', text)  # Removes hash symbols.
    text = re.sub('RT[\s]+', '', text)  # Removes retweet symbols.
    text = re.sub(r'https?:\/\/\S+', '', text)  # Removes URLs.
    return text


df['Review'] = df['Review'].apply(cleanTxt)  # Applies the cleanTxt function to each review in the DataFrame.

print(df)

afinn = Afinn()  # Creates an instance of the Afinn class.
positive = []
negative = []
neutral = []

for review in df['Review']:
    if afinn.score(review) > 0:
        positive.append(review)
    if afinn.score(review) < 0:
        negative.append(review)
    if afinn.score(review) == 0:
        neutral.append(review)

print("positive reviews:", positive, "\t\n")
print("negative reviews: ", negative, "\t\n")
print("neutral reviews: ", neutral, "\t\n")

total_reviews = len(df["Review"])
print("total number of review: ", total_reviews)
print('number of positive reviews : ', len(positive))
print('number of negative reviews : ', len(negative))
print("number of neutral reviews : ", len(neutral))
