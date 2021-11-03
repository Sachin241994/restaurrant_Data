#!/usr/bin/env python
# coding: utf-8

"""
[7:34 PM, 10/3/2021] Sachin Dabas: Write a python script to pull some required information from a web page

2. Clean the pulled informationand store it in a csv file

3. The python script should take url as input and output the csv file with pulled, cleaned required information.





Restaurant Web page url: https://www.yelp.ca/biz/pai-northern-thai-kitchen-toronto-5?osq=Restaurants



It lists information about the restaurant.



Information required from the page: 

Name of the restaurant

How many reviews are there in total

Reviews

  - Review_text

  - Reviewer

  - Rating
[7:39 PM, 10/3/2021] Sachin Dabas: 1. Write a python script to pull some required information from a web page

2. Clean the pulled informationand store it in a csv file

3. The python script should take url as input and output the csv file with pulled, cleaned required information.





Restaurant Web page url: https://www.yelp.ca/biz/pai-northern-thai-kitchen-toronto-5?osq=Restaurants



It lists information about the restaurant.



Information required from the page: 

Name of the restaurant

How many reviews are there in total

Reviews

  - Review_text

  - Reviewer

  - Rating
  
  """ 

# In[13]:


import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


# In[2]:


def get(url):
    try:
        response = requests.get(url, stream=True)
    except requests.HTTPError:
        return None
    if response.status_code == 200:
        return response
    return None


# In[3]:


def mining_review(base_url):
    all_reviews = list()
    for page in range(0, 20, 10):
        review_url = base_url + f'&start={page}'
        response = get(review_url)
        if response:
            soup = BeautifulSoup(response.content, 'html.parser')
            reviews = soup.find_all('div', attrs={'class': 'review__373c0__3MsBX border-color--default__373c0__1WKlL'})
            if len(reviews) != 0:
                for review in reviews:
                    comment = review.find('p', attrs={'class': 'comment__373c0__Nsutg css-n6i4z7'})
                    name = review.find('span', attrs={'class': 'fs-block css-m6anxm'})
                    all_reviews.append({'name': name.text, 'comment': comment.text})

    return all_reviews


# In[4]:


def mining_information(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    restaurant_name = soup.find('h1', attrs={'class': 'css-m7s7xv'})
    all_reviews = mining_review(response.url)
    data = {'restaurant_name': restaurant_name.text, 'total_comments': len(all_reviews), 'comments': all_reviews ,}
    return data


# In[9]:


def start():
    response = get('https://www.yelp.ca/biz/pai-northern-thai-kitchen-toronto-5?osq=Restaurants')
    
    return mining_information(response)


# In[10]:


data=start()


# In[11]:


data


# In[14]:


res=pd.DataFrame(data)


# In[16]:


res.to_csv("yelp_restaurant.csv")


# In[ ]:




