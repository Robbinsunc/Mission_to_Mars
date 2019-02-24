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
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser =  Browser('chrome', **executable_path, headless=False)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemi_html = browser.html
    soup = bs(hemi_html, "html.parser")

    hemi = soup.find('div', 'collapsible results')
        
    mars_hemi_image = hemi.find_all("div", {"class": "description"})
    hemisphere_image_urls = []

    for image in mars_hemi_image:
        attrib = image.find('a')

        #Retrieve title and link to specific hemisphere page
        title = attrib.h3.text
        link = 'https://astrogeology.usgs.gov' + attrib['href']

        #Visit above link
        browser.visit(link)
        time.sleep(2)

        #Retrieve link to image
        html = browser.html
        hemi_soup = bs(html, 'html.parser')
        image_link = hemi_soup.find('div', 'downloads').find('li').a['href']

        #Create empty dictionary for title & image
        hemi_dict = {}
        hemi_dict['title'] = title
        hemi_dict['img_url'] = image_link

        #Add image_dict to empty list from above
        hemisphere_image_urls.append(hemi_dict)

    
    return mars_data




