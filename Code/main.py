from bs4 import BeautifulSoup
from argparse import Namespace
from urllib.request import urlopen
import pandas as pd
import re
import nltk
#nltk.download()
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
import tkinter as tk

##Web scraping
def get_genres(soup):
    genres = []
    for node in soup.find_all('div', {'class': 'left'}):
        current_genres = node.find_all('a', {'class': 'actionLinkLite bookPageGenreLink'})
        current_genre = ' > '.join([g.text for g in current_genres])
        if current_genre.strip():
            genres.append(current_genre)
    return genres


def scrape_book(book_id: str, args: Namespace):
    url = "https://www.goodreads.com/book/show/" + book_id
    source = urlopen(url)
    soup = BeautifulSoup(source, "html.parser")
    desc = soup.find("span", {"class": "Formatted"}).text;

    book = {
        "book_description": desc,
    }
    return book


##lematization
def get_part_of_speech_tags(token):
#We are focusing on Verbs, Nouns, Adjectives and Adverbs here.
 tag_dict = {"J": wordnet.ADJ,
 "N": wordnet.NOUN,
 "V": wordnet.VERB,
 "R": wordnet.ADV}

 tag = nltk.pos_tag([token])[0][1][0].upper() #eg. from [('She', 'PRP')] get P
 return tag_dict.get(tag, wordnet.NOUN)
# if no match, return Noun as the POS


##GUI
def submit():
    userIn = prompt.get()
    output.configure(state='normal')
    output.delete(1.0, tk.END)
    book = scrape_book(userIn, args="")
    description = book["book_description"]
    output.insert(tk.END, description)
    output.configure(state='disabled')

    file = open("results.txt", "w")
    file.write(userIn + ': ' + str(description))
    file.close()


    finalToken = str(description).split();

    file = open("Tokenizer.txt", "w")
    file.write(userIn + ': ' + str(finalToken))
    file.close()

    #countVectoriser
    vectorizer = CountVectorizer(stop_words='english')
    X_vec = vectorizer.fit_transform(finalToken)
    vector_desc = vectorizer.vocabulary_

    file = open("vectoriser.txt", "w")
    file.write(str(vector_desc))
    file.close()

    ##lematization
    lemmatizer = WordNetLemmatizer()

    temp = []
    for token in finalToken:
        lemmatisedtoken = lemmatizer.lemmatize(token, get_part_of_speech_tags(token))
        temp.append(lemmatisedtoken)

    file = open("lemmatized.txt", "w")
    file.write(userIn + ': ' + str(temp))
    file.close()





def open_about_window():
    about_window = tk.Toplevel(root)  # Create a new Toplevel window
    about_window.title("About")  # Set the title of the window
    about_label = tk.Label(about_window, text="To start searching for the book's description, enter the book ID located in the URL of the book. \n \n Example: 4667024 (The Help by Kathryn Stockett). \n\n The description of the book will be shown in the output panel after the ID is entered and the submit button is pressed. \n\n Due to the description being webscraped, running the program a lot of times in a row might cause the goodreads servers to block the IP coming from the user using this program. \n You will be able to use it after some time again in the case you are blocked temporarily.   ")  # Create a label with some text
    about_label.pack()  # Add the label to the window

root = tk.Tk()
root.title("Text Box Example")

# Create the main menu bar
menubar = tk.Menu(root)

# Create the Help menu
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=open_about_window)  # Add an "About" option to the menu
menubar.add_cascade(label="Help", menu=help_menu)  # Add the Help menu to the main menu bar

root.config(menu=menubar)  # Set the menu bar for the main window

prompt_label = tk.Label(root, text="Enter prompt:")
prompt_label.pack()

prompt = tk.Entry(root)
prompt.pack()

output_label = tk.Label(root, text="Output:")
output_label.pack()

output = tk.Text(root, height=10, state='disabled')
output.pack()

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

root.mainloop()
