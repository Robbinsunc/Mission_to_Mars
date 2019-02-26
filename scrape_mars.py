#!/usr/bin/env python
# coding: utf-8


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from selenium import webdriver
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time


def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser =  Browser('chrome', **executable_path, headless=False)
    
    #dictionary to store mars data
    mars_data = {}

    # Nasa Mars News:
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)


    html = browser.html
    soup = bs(html, "html.parser")


    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    #store scrape news in mars dictionary
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p         


    #JPL Mars Space Images - Featured Image
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser =  Browser('chrome', **executable_path, headless=False)
    
    jpl_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_image)

    html= browser.html
    soup = bs(html, "html.parser")
    #browser.click_link_by_partial_text('FULL IMAGE')

    featured_image = soup.find("div", class_="carousel_items").find("article")["style"]


    featured_image_url = featured_image.split("'")[1]
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url
    
    #store featured image in mars dictionary
    mars_data['featured_image_url'] = featured_image_url


    #Mars Weather
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser =  Browser('chrome', **executable_path, headless=False)
    
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)

    html = browser.html
    soup = bs(html, "html.parser")
    #print(soup.prettify())


    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    
    #store mars weather in mars dictionary
    mars_data['mars_weather'] = mars_weather

    #Mars facts
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser =  Browser('chrome', **executable_path, headless=False)
    
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(mars_facts_url)
    mars_facts_df = mars_facts[0]
    #mars_facts_df

    mars_facts_df.columns = ["Description", "Fact"]
    

    #dataframe to html
    mars_facts = mars_facts_df.to_html()
    
    #store mars facts in mars dictionary
    mars_data['mars_facts'] = mars_facts

    #Mars Hemisphere images
    #Mars Hemispheres
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser =  Browser('chrome', **executable_path, headless=False)
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)
    
    html = browser.html
    soup = bs(html, "lxml")
    
    hemi_image = soup.find_all('div', class_='item')
    hemisphere_image_urls = []

    image_base = "https://astrogeology.usgs.gov"

    for image in hemi_image:
    
        #Retrieve title and link to specific hemisphere page
        title = image.find('h3').text
    
        image_base2 = image.find('a', class_='itemLink product-item')['href']

        #Visit above link
        browser.visit(image_base + image_base2)

        #visit link to full image
        image_html = browser.html
        hemi_soup = bs(image_html, 'html.parser')
        img_url = image_base + hemi_soup.find('img', class_='wide-image')['src']

        #Add images dictionary to list
        hemisphere_image_urls.append({'title': title, "img_url": img_url})
        
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls


    
    return mars_data

    browser.quit()




