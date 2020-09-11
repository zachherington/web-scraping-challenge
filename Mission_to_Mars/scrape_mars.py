# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import pymongo

# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)
# db = client.mars_db
# mars_db = db.mars_db



#### Open Chromedriver
def init_browser():
    executable_path = {'executable_path': '.\\resources\\chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)


#### Scrape Web Data
def scrape():
    browser = init_browser()

    ## Data Scraping NASA's News Page ##
    # Opens web page
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_url)
    
    html = browser.html
    nasa_soup = bs(html, 'html.parser')

    # Find the Latest News Headline 
    latest_headline = nasa_soup.find_all('div',class_ = 'content_title')[1].text
    headline_desc = nasa_soup.find('div', class_ = 'article_teaser_body').text



    ## Data Scraping JPL's Space Image Page ##
    # Find the JPL Featured Image
    jpl_base_url = 'https://www.jpl.nasa.gov'
    jpl_home_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_home_url)

    # Navigate to Full Image Url
    browser.click_link_by_id(id = 'full_image')
    browser.click_link_by_partial_text('more info')

    html = browser.html
    jpl_soup = bs(html, 'html.parser')

    full_image_path = jpl_soup.find(class_ = 'main_image')["src"]

    featured_image_url = f'{jpl_base_url}{full_image_path}'



    ## Data Scraping Mars Facts ##
    facts_url = "https://space-facts.com/mars/"

    browser.visit(facts_url)
    html = browser.html

    facts_soup = bs(html, 'html.parser')

    # Use pandas to scrape mars facts
    mars_facts = pd.read_html(facts_url)[0]
    mars_facts.columns = ['Measure', 'Value']
    mars_facts.set_index('Measure', inplace = True)
    
    # Format as html table string and save as 'mars_facts.html'
    mars_facts_html = mars_facts.to_html(classes= "table table-striped")



    ## Data Scraping Mars Hemisphere Images ##
    hemi_base_url = "https://astrogeology.usgs.gov"
    hemi_home_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(hemi_home_url)
    html = browser.html

    hemi_soup = bs(html, 'html.parser')

    # Save HD image url string and corresponding titles
    all_hemi_sections = hemi_soup.find_all(class_ = 'description')
    all_hemi_sections

    hemi_list = []

    for hemi in all_hemi_sections:
        
        # Find Titles for Hemishperes
        hemi_title = hemi.find('h3').text
        
        # Navigate to next page urls
        hemi_nextpage = hemi.find('a')['href']
        browser.visit(hemi_base_url + hemi_nextpage)

        html2 = browser.html
        image_soup = bs(html2, 'html.parser')

        # Finds the HD image urls
        image_section = image_soup.find(class_ = 'downloads')
        hemi_image = image_section.find('li').a['href']

        # Stores results to a dict so we can append 'hemi_list'
        hemi_dict = {}
        hemi_dict['hemi_title'] = hemi_title
        hemi_dict['hemi_image'] = hemi_image

        hemi_list.append(hemi_dict)

        mars_data = {
            'latest_headline': latest_headline,
            'headline_desc':headline_desc,
            'featured_image_url': featured_image_url,
            'facts_html': mars_facts_html,
            'hemi_list': hemi_list
        }

    return mars_data

if __name__ == '__main__':
    scrape()