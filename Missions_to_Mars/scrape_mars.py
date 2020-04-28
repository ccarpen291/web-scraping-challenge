# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import time
import pymongo
import requests
from time import sleep
from IPython.display import Image
import pandas as pd
import os

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)
    return Browser("chrome", headless=True) #headless = true means no browser

def scrape():
    mars = {}
    # URL of page to be scraped
    browser = init_browser()
    #url = 'https://mars.nasa.gov/news/'
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    #content_title was in the original html
    if browser.is_element_present_by_css('div.content_title', wait_time=4):
        #First look for all of the html
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        #what we are looking for is in a div, nested deep in a title
        results = soup.find_all('div', class_='content_title')
        #We do .text becasue we are pulling out the html text deep listed
        news_title = results[1].text
        #This will return a list for the article teaser body, which comes from the html code
        results = soup.find_all('div', class_='article_teaser_body')
        #This does not have a nested anchor so we will do results 0 here
        news_paragraph = results[0].text
        print(news_paragraph)
        print(' ')
        print(news_title)
        #Save information to a diciontary
        mars.update({"Latest Mars News Title":news_title,"Latest Mars News":news_paragraph})

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    results = browser.find_by_id('full_image')
    img = results[0]
    #here we are looking for a feature image
    #This clicks on the button "full Image" to take you to the website
    img.click()
    sleep(4)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    featured_image_url = soup.find("img", class_="fancybox-image")["src"]
    base_url = 'https://www.jpl.nasa.gov'
    full_featured_image_url = (f'{base_url}{featured_image_url}')
    print(full_featured_image_url)
    mars.update({"Featured Mars Image":full_featured_image_url})


    #Go to twitter and save the latest tweet for mars weather and save as 'mars_weather'
    url = 'https://twitter.com/marswxreport?lang=en'
    #this visits the url
    browser.visit(url)
    #web scraping via splinter
    #Went to first tweet on the above website, inspect then copy from xpath and selected copy from xpath
    #this xpath corresponds directly to the URL
    xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div/div/div/div/div/div[2]/section/div/div/div[1]/div/div/div/article/div/div[2]/div[2]/div[2]/div[1]/div/span'
    #We found xpath from twitter, navigating to the first tweet, right click and copy full xpath
    #this activates silenium, with a wait time of 10 seconds to let the page load
    #This is the line that checks to exist it's real
    # x paths are helpful to drill down to the item that we need
    if browser.is_element_present_by_xpath(xpath, wait_time=5):
        #Select the html element we copied above
        first_tweet = browser.find_by_xpath(xpath)
        #if we wanted to click, we could do first_tweet.click()
        #this is the html of the first tweet
        html = first_tweet.html
        #Pass just the html we want to Beautiful Soup to return the result
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.prettify())
        #Method 2
        print(first_tweet.text)
        mars_weather = str(first_tweet.text)
        mars.update({"Latest Mars Weather":mars_weather})


    #use pandas to scrape and return mars facts
    #Pandas only looks for tables when web scraping
    #It will ignore everything else
    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')
    #This pulls the first table on the webpage, you can see other tables by changing 0,1,2,3 etc
    mars_facts = pd.read_html(soup.prettify())[0]
    #save the html file, makes a file on our file on the local computer
    mars_html = mars_facts.to_html(index = False)
    print(mars_facts)
    mars.update({"Mars Fun Facts":mars_html})


    #want to get high resolution of the images from mars and save them down
    #Goal is to save image url string
    #Save the hemisphere title
    #save in a dictionary, using keys 'img_url' and 'title'
    browser = init_browser()
    #Url that we want to scrape
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #Visit the url
    browser.visit(url)
    time.sleep(4)
    #This is the raw html code
    html = browser.html
    #putting it in soup so we can better parse it out
    soup = BeautifulSoup(html, 'html.parser')
    #Find the first link that we are looking to click This will return a list
    #Find the text that we want to click, this will come from the html and we know it's a text becasue its listed as a text in the html file
    results = browser.find_by_text('Cerberus Hemisphere Enhanced')
    #print(results)
    #Not necessary but can be saved, second method
    #img = results[0]
    #this is correct, second method
    #img.click()
    #This advances to the next webpage
    results.click()
    time.sleep(4)
    #Grab the html on the next webpage
    html = browser.html
    #Pass to the soup
    soup = BeautifulSoup(html, 'html.parser')
    #Find the correct html code
    #Find all returns everything in a list
    #instead find gets the first one
    results = soup.find_all('div', class_='downloads')
    #Further cull down the anchor of the results
    cerberus_link = results[0].find('li').a['href']
    print("Cerberus link is")
    print(cerberus_link)
    soup = BeautifulSoup(html,'html.parser')
    #When you use "find" that gets you a non list
    #When you use find all that gets you a list of everything tha tis found so you will need to do do title[0]
    cerberus_title = soup.find('h2', class_='title').text
    print("Cerberus title is ")
    print(cerberus_title)
    #Create the dictionary to store the information
    cerberus={"title":cerberus_title,"image_url":cerberus_link}
    #Url that we want to scrape
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #Visit the url
    browser.visit(url)
    time.sleep(4)
    #This is the raw html code
    html = browser.html
    #putting it in soup so we can better parse it out
    soup = BeautifulSoup(html, 'html.parser')
    #Find the first link that we are looking to click This will return a list
    #Find the text that we want to click, this will come from the html and we know it's a text becasue its listed as a text in the html file
    Schiaparelli_results = browser.find_by_text('Schiaparelli Hemisphere Enhanced')
    Schiaparelli_results.click()
    time.sleep(4)
    #Grab the html on the next webpage
    html = browser.html
    #Pass to the soup
    soup = BeautifulSoup(html, 'html.parser')
    #Find the correct html code
    #Find all returns everything in a list
    #instead find gets the first one
    results = soup.find_all('div', class_='downloads')
    #Further cull down the anchor of the results
    Schiaparelli_link = results[0].find('li').a['href']
    print("Link is")
    print(Schiaparelli_link)
    soup = BeautifulSoup(html,'html.parser')
    #When you use "find" that gets you a non list
    #When you use find all that gets you a list of everything tha tis found so you will need to do do title[0]
    Schiaparelli_title = soup.find('h2', class_='title').text
    print("title is")
    print(Schiaparelli_title)
    schiaparelli={"title":Schiaparelli_title,"image_url":Schiaparelli_link}
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #Visit the url
    browser.visit(url)
    time.sleep(4)
    #This is the raw html code
    html = browser.html
    #putting it in soup so we can better parse it out
    soup = BeautifulSoup(html, 'html.parser')
    #Find the first link that we are looking to click This will return a list
    #Find the text that we want to click, this will come from the html and we know it's a text becasue its listed as a text in the html file
    Syrtis_results = browser.find_by_text('Syrtis Major Hemisphere Enhanced')
    Syrtis_results.click()
    time.sleep(4)
    #Grab the html on the next webpage
    html = browser.html
    #Pass to the soup
    soup = BeautifulSoup(html, 'html.parser')
    #Find the correct html code
    #Find all returns everything in a list
    #instead find gets the first one
    results = soup.find_all('div', class_='downloads')
    #Further cull down the anchor of the results
    Syrtis_link = results[0].find('li').a['href']
    print(Syrtis_link)
    soup = BeautifulSoup(html,'html.parser')
    #When you use "find" that gets you a non list
    #When you use find all that gets you a list of everything tha tis found so you will need to do do title[0]
    Syrtis_title = soup.find('h2', class_='title').text
    print(Syrtis_title)
    syrtis={"title":Syrtis_title,"image_url":Syrtis_link}
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #Visit the url
    browser.visit(url)
    time.sleep(4)
    #This is the raw html code
    html = browser.html
    #putting it in soup so we can better parse it out
    soup = BeautifulSoup(html, 'html.parser')
    #Find the first link that we are looking to click This will return a list
    #Find the text that we want to click, this will come from the html and we know it's a text becasue its listed as a text in the html file
    Valles_results = browser.find_by_text('Valles Marineris Hemisphere Enhanced')
    Valles_results.click()
    time.sleep(4)
    #Grab the html on the next webpage
    html = browser.html
    #Pass to the soup
    soup = BeautifulSoup(html, 'html.parser')
    #Find the correct html code
    #Find all returns everything in a list
    #instead find gets the first one
    results = soup.find_all('div', class_='downloads')
    #Further cull down the anchor of the results
    Valles_link = results[0].find('li').a['href']
    print(Valles_link)
    soup = BeautifulSoup(html,'html.parser')
    #When you use "find" that gets you a non list
    #When you use find all that gets you a list of everything tha tis found so you will need to do do title[0]
    Valles_title = soup.find('h2', class_='title').text
    print(Valles_title)
    valles={"title":Valles_title,"image_url":Valles_link}
    hemisphere_image_urls=[cerberus,schiaparelli,syrtis,valles]
    mars.update({"Mars Hemispheres":hemisphere_image_urls})
    return mars


if __name__ == "__main__":
    print(scrape())