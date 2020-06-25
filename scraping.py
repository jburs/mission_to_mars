
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

# Set the executable path and initialize the chrome browser in splinter
def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    
    # Run all scraping functions and store results in dictionary
    news_title, news_paragraph = mars_news(browser)
    mars_hemispheres_info = mars_hemisphere(browser)
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_0_link": mars_hemispheres_info[0]['img_url'], 
        "hemisphere_0_title":mars_hemispheres_info[0]['title'],
        "hemisphere_1_link": mars_hemispheres_info[1]['img_url'], 
        "hemisphere_1_title":mars_hemispheres_info[1]['title'],
        "hemisphere_2_link": mars_hemispheres_info[2]['img_url'], 
        "hemisphere_2_title":mars_hemispheres_info[2]['title'],
        "hemisphere_3_link": mars_hemispheres_info[3]['img_url'], 
        "hemisphere_3_title":mars_hemispheres_info[3]['title']
    }
    browser.quit()
    return data


def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
    
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except:
        return None, None

    return news_title, news_p


# Featured Images
# Visit URL

def featured_image(browser):

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try: 
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        # Use the base URL to create an absolute URL
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    except AttributeError:
        return None

    return img_url


def mars_facts():

    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


def mars_hemisphere(browser):
    # Visit URL, create lists to store links and titles
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # list to store links and titles for hemispheres
    mars_hemispheres = []

    #find by partial returns 8 potential links. links 1, 3, 5, 7 are used
    for i in range(1,9,2):
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        links_found = browser.links.find_by_partial_href('/search/map/Mars/')
        links_found[i].click()
        #parse html, find link, and corresponding title
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        zero_link = img_soup.find("div", class_='downloads')
        link = zero_link.find('a')['href']
        title = img_soup.find("h2", class_='title').text
        mars_hem = {"img_url":link, "title":title}
        mars_hemispheres.append(mars_hem)
    
    return(mars_hemispheres)



if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


