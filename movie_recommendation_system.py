import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import os

"""
Works for imdb pages recommend using all the pages with genres information discards all the ones with less than 3 genres type
"""

def post_process(genres):
    post_process_genres = []
    for  i in genres:
        i = i.replace("\n","")
        i = i.replace(" ", "")
        post_process_genres.append(i)
    return post_process_genres

# def check_repeated_coma(x):
#     list_x = x.split(',')


def get_all_genres(soup):
    result_genres=[]
    all_genres= soup.find_all("p",{"class":"text-muted"})
    print(all_genres)

    ##################################################################3

    for genre in all_genres:
        genre = str(genre.find_all("span",{"class":"genre"}))
        if genre =='[]':
            pass
        else :
            genre = genre.replace("<","=")
            genre = genre.replace(">","=")
            genre = genre.split('=')
            genre = genre[int(len(genre)/2)]
            result_genres.append(genre)
    print(result_genres)
    return result_genres

def get_all_titles(soup):
    result_topics = []
    # * only for urls with lists
    all_topics = soup.find_all('h3',{"class":"lister-item-header"})
    for topic in all_topics:
        topic_a = topic.find('a')
        # ? Sir method
        # topic = str(topic.find('a'))
        # topic = topic.replace("<","=")
        # topic = topic.replace(">","=")
        # topic = topic.split('=')
        # topic = topic[int(len(topic)/2)]
        # result_topics.append(topic)
        result_topics.append(topic_a.getText())
    return result_topics

def check_repeated_comma(x):
    list_x = x.split(',')
    if len(list_x)==3:
        return x
    else:
        return np.nan

def data_set(url):
    data_set = pd.DataFrame(columns=["Movie","Primary Genre","Secondary Genre","Tertiary Genre"])
    # Initially get the page from the url and from the content extract all the things properly so page is extracted
    page=requests.get(url)

    # Soup is created where all the content is parsed as html format for so it can be extracted as seen in webpages
    soup = BeautifulSoup(page.content,'html.parser')
    title = get_all_titles(soup)
    print(title)

    genres = get_all_genres(soup)
    print(genres)
    genres = post_process(genres)
    data_set["Movie"] = pd.Series(title)
    data_set["Primary Genre"] = pd.Series(genres)
    data_set["Primary Genre"] = data_set["Primary Genre"].apply(check_repeated_comma)
    data_set["Secondary Genre"] = data_set["Secondary Genre"].fillna('To Be filled')
    data_set["Tertiary Genre"] = data_set["Tertiary Genre"].fillna('To Be filled')
    # print(data_set)
    data_set = data_set.loc[data_set['Primary Genre']!= np.NaN]
    data_set = data_set.dropna(how = "any")
    data_set[["Primary Genre","Secondary Genre","Tertiary Genre"]] = data_set["Primary Genre"].str.split(',',expand = True)
    print(data_set)
    data_set.to_csv("Dataset.csv", mode = 'a' , header = False)


# main part
os.system('clear')
print('----------------------------------- IMDB Scraper -----------------------------------------------')
number_of_pages = int(input('Enter the number of various pages to scrape: '))
for i in range(number_of_pages):
    url = input('Enter the url: ')
    data_set(url)