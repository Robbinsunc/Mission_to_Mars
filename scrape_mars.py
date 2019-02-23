#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time

# In[2]:

def init_browser():
    executable_path = {'executable_path': '/Users/JoeRobbins/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


# In[3]:

def scrape():
    browser = init_browser()
# Nasa Mars News:
# URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

# In[4]:


    html = browser.html
    soup = bs(html, "html.parser")


# In[5]:


    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    print(news_title)
    print(news_p)


# In[6]:


    #JPL Mars Space Images - Featured Image
    jpl_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_image)


# In[7]:


    html= browser.html
    soup = bs(html, "html.parser")
#browser.click_link_by_partial_text('FULL IMAGE')


# In[8]:


    featured_image = soup.find("div", class_="carousel_items").find("article")["style"]


# In[9]:


    featured_image_url = featured_image.split("'")[1]
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url
    print(featured_image_url)


# In[10]:


#Mars Weather
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)


# In[11]:


    html = browser.html
    soup = bs(html, "html.parser")
#print(soup.prettify())


# In[12]:


    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)


# In[13]:


#Mars facts
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(mars_facts_url)
    mars_facts_df = mars_facts[0]
    mars_facts_df


# In[14]:


    mars_facts_df.columns = ["Description", "Fact"]
    mars_facts_df.set_index("Description")


# In[22]:


    mars_table = mars_facts_df.to_html()
    mars_table.replace('\n', '')


# In[24]:


    mars_facts_df.to_html('mars_table.html')


# In[25]:


#Mars Hemispheres
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)


# In[26]:


    html = browser.html
    soup = bs(html, "lxml")


# In[31]:


    mars_hemi_image = soup.find_all("div", class_="item")
    hemisphere_image_urls = []

    for image in mars_hemi_image:
        hemi_dict = {}
    
        hemi_image = image.find("a", class_="itemLink product-item")
        link = "https://astrogeology.usgs.gov/" + hemi_image['href']
        #print(link)
    
        browser.visit(link)
    
        html = browser.html
        hemi_soup = bs(html, 'html.parser')
    
        hemi_title = hemi_soup.find('div', class_='content').find('h2', class_='title').text
        hemi_dict["title"] = hemi_title
    
        hemi_img = hemi_soup.find('div', class_='downloads').find('a')['href']
        hemi_dict['img_url'] = hemi_img
    
        hemisphere_image_urls.append(hemi_dict)
    
    hemisphere_image_urls

    # Store data in a dictionary
    mars_data = {}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
# In[ ]:




