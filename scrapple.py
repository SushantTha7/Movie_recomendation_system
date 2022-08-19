import os
import pandas as  pd
import requests
from bs4 import BeautifulSoup
import numpy as np




def get_all_titles(soup):
    result_topics = []

    #only for urls with lists
    all_topics = soup.find_all('h3',{"class":"lister-item-header"})
    # print(all_topics)
    # ###all_topics = soup.find_all('h3',{"class":"lister-item-header"})

    for topic in all_topics:
        topic_a = topic.find('a') 
        # topic= str(topic.find('a')) 
        # sir ko methode
        # topic= topic.replace("<","=")
        # topic= topic.replace(">","=")
        # topic topic.split("=")
        # topic = topic[int[len(topic)/2]]
        # result_topics.append(topic)
        result_topics.append(topic_a.getText())
    return result_topics


def get_all_genres(soup):
    result_genres=[]
    all_genres = soup.find_all("p",{"class":'text-muted'})
    print(all_genres)
    for genre in all_genres:
        genre = str(genre.find_all("span",{"class":"genre"}))
        if genre=='[]':
            pass
        else:
            genre=genre.replace("<","=")
            genre=genre.replace(">","=")
            genre=genre.split("=")
            genre=genre[int((len(genre)/2))]
            result_genres.append(genre)
    print (result_genres)
    return result_genres

##############



def post_process(genres):
    post_process_genres=[]
    for i in genres:
        i = i.replace("\n","")
        i = i.replace(" ","")
        post_process_genres.append(i)
    return post_process_genres




########################

def data_set(url):
    data_set = pd.DataFrame(columns=["Movie","Primary Genre","Secondary Genre","Tertiary Genre"])
    #initailly we get the page from  and from the context above thigs are extracted
    page = requests.get(url)

    #soup created where all the content is parsed as hm=tml format for so it can be extracted as seen in web pages
    soup = BeautifulSoup(page.content,'html.parser')
    print(soup)      #prints the code of the url 
    title = get_all_titles(soup)
    print(title)
    genres = get_all_genres(soup)
    print(genres)
    genres = post_process(genres)
    data_set["Movie"] = pd.Series(title)
    data_set["Primary Genre"] = pd.Series(genres)
    data_set["Primary Genre"]= data_set["Primary Genre"].apply(check_repeated_comma)
    data_set["Secondary Genre"] = data_set["Secondary Genre"].fillna("to be filled")
    data_set['Tertiary Genre'] = data_set['Tertiary Genre'].fillna('to be filled')
    data_set = data_set.loc[data_set["Primary Genre"]!=np.nan]    
    data_set = data_set.dropna(how = "any")
    data_set[["Primary Genre","Secondary Genre","Tertiary Genre"]] = data_set["Primary Genre"].str.split(',',expand = True)

    # data_set[['Primary Genre','Secondary Genre','Tertiary Genre']]=data_set['Primary Genre'].str.split(',' , expand = True)
    data_set.to_csv("Data_set.csv",mode='a',header = False )
    print (data_set)

##############

def check_repeated_comma(x):
    list_x = x.split(',')
    if len(list_x)==3:
        return x
    else:
        return np.nan

    

#main part

os.system('clear')
print("IMDB Scrapper")
number_of_pages=int(input('enter the number of various pages to scrap:'))
for i in range(number_of_pages):
    url = input ('enter the url:')
    data_set(url)
    
#https://m.imdb.com/chart/top/?ref_=nv_mv_250