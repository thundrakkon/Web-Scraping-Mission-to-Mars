import datetime
import os
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # URL of Mars News from NASA
    url_nasa_news = "https://mars.nasa.gov/news/"
    browser.visit(url_nasa_news)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    # Title and paragraph text of 1st news article
    div = soup.find_all('div', class_='image_and_description_container')[0]
    a = div.find('a')
    href = a['href']
    url_news = 'https://mars.nasa.gov' + href
    browser.visit(url_news)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('h1', class_='article_title').text
    news_p = soup.find('i').text
    
    # URL of the Mars Space Images and open in browser
    url_mars_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_mars_images)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    # Image title
    images = soup.find('div', class_='carousel_items')
    article = images.find('article')
    img_title = article['alt']
    
    # Image link
    featured_image_relative_path = article['style'].split("url('")[1].split("')")[0]
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_relative_path

    # Define Mars Weather URL and open in browser
    url_mars_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_mars_weather)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find the first tweet message
    tweet_overall = soup.find_all('div', class_='css-1dbjc4n')[0]
    tweet_div = tweet_overall.find_all('div', class_='css-901oao')[26]
    mars_weather = tweet_div.find('span', class_='css-901oao').text

    # Define URL for Mars facts
    url_mars_fact = 'https://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    tables = pd.read_html(url_mars_fact)
    time.sleep(1)

    # Converting the 1st table into a DataFrame
    df_table = tables[0]

    # Adding column names
    df_table.columns= ['description', 'value']

    # Listing the row names
    df_table.rows = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons', 
              'Orbit Distance', 'Orbit Period', 'Surface Temperature', 'First Record', 
              'Recorded By']

    # Setting the "description" column as the index
    df_table.set_index('description', inplace=True)

    # Generating the DataFrame into a HTML table
    html_table = df_table.to_html()

    # Cleaning the table by stripping unnecessary codes
    html_table = html_table.replace('\n', '')


    # Define Mars Hemisphese URL and open in browser
    url_mars_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_mars_hemispheres)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Create an empty list for the images dictionary
    hemisphere_image_urls = []

    # Locate where the images and titles are for each image
    div = soup.find_all('div', class_='item')

    # Loop through for each hemisphere page
    for d in div:
        a = d.find('a')
        href = a['href']
        # Identify each hemisphere URL
        url = 'https://astrogeology.usgs.gov' + href

        # Load the hemisphere page to be scraped
        url_mars_one_hemisphere = url
        browser.visit(url_mars_one_hemisphere)
        html = browser.html
        soup = bs(html, 'html.parser')

        # Locate the image
        container = soup.find('div', class_='wide-image-wrapper')
        img = container.find('img', class_='wide-image')
        src = img['src']

        # Create the image links
        img_url = 'https://astrogeology.usgs.gov' + src
        # Identify the title
        title = soup.find('h2', class_='title').text
    
        # Define the keys for the dictionary
        keys_dict = {'title': title, 'img_url': img_url}
        # Append the dictionary
        hemisphere_image_urls.append(keys_dict)

        # Give the website a 3 second break before scraping again
        time.sleep(3)
    
    image_01 = hemisphere_image_urls[0]

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "img_title": img_title,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }
    # Close the browser after scraping
    browser.quit()
    
    # Return results
    return mars_data

