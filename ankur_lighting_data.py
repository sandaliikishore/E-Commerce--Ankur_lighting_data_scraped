from bs4 import BeautifulSoup
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def make_request(url):
    """
    Make an HTTP GET request to the specified URL with retry logic.

    Parameters:
        url (str): The URL to fetch.

    Returns:
        Response: The HTTP response object if the request succeeds.
        None: If the request fails after retries.
    """
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {url}: {e}")
        return None

def get_category_urls(category):
    """
    Generate a list of all page URLs for a given product category.

    Parameters:
        category (str): The category name to scrape.

    Returns:
        list: A list of URLs for all pages in the category.
    """
    category_urls = []
    page_number = 1
    while True:
        url = f"{base_url}/collections/{category}?page={page_number}"
        response = make_request(url)
        if response is None:
            break
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Check if there are products on the page
        product_links = soup.find_all("a", class_="product-title h6")
        if not product_links:
            break
        
        category_urls.append(url)
        page_number += 1
    
    return category_urls

# Define the base URL for the website
base_url = "https://www.ankurlighting.com"

# Define the product categories to scrape
categories = ["chandeliers", "table-lamps", "wall-lights", "pendant-lights", "floor-lamps", "outdoor-lights", "ceiling-lights", "architectural-lights"]

# Initialize a dictionary to store the scraped data
data = {"category": [], "title": [], "price": [], "img_url": []}

def extract_data(soup, selector, attribute=None):
    """
    Extract data from HTML elements using a CSS selector.

    Parameters:
        soup (BeautifulSoup): The parsed HTML content.
        selector (str): The CSS selector to locate elements.
        attribute (str, optional): The attribute to extract. Defaults to None.

    Returns:
        list: A list of extracted text or attribute values.
    """
    elements = soup.select(selector)
    if attribute:
        return [elem.get(attribute, "").strip() for elem in elements]
    return [elem.get_text(strip=True) for elem in elements]

def get_product_details(soup):
    """
    Extract detailed product specifications from the product page.

    Parameters:
        soup (BeautifulSoup): The parsed HTML content of the product page.

    Returns:
        dict: A dictionary of product specifications.
    """
    product_details = {}
    table = soup.find("table", class_="spec__table")
    if table:
        rows = table.find_all("tr")
        for row in rows:
            key = row.find("th", class_="attr__label").get_text(strip=True)
            value = row.find("td", class_="attr__value").get_text(strip=True)
            product_details[key] = value
    return product_details

# Iterate over each product category
for category in categories:
    category_urls = get_category_urls(category)  # Get all URLs for the category
    for url in category_urls:
        response = make_request(url)
        if response is None:
            continue
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all product links on the page
        product_links = soup.find_all("a", class_="product-title h6")
        links_list = [link.get('href') for link in product_links]
        
        # Iterate over each product link to extract details
        for link in links_list:
            product_url = base_url + link
            product_response = make_request(product_url)
            if product_response is None:
                continue
            product_soup = BeautifulSoup(product_response.content, "html.parser")

            # Extract product title, price, and image URL
            titles = extract_data(product_soup, "h1.product-title.h3")
            prices = extract_data(product_soup, "span.money.conversion-bear-money")
            img_urls = extract_data(product_soup, "div.product-gallery__media:nth-child(1) > img:nth-child(1)", "src")

            # Append the extracted data to the respective fields
            data['category'].append(category)
            data['title'].append(titles[0] if titles else "")
            data['price'].append(prices[0] if prices else "")
            data["img_url"].append(img_urls[0] if img_urls else "")

            # Extract additional product details
            product_details = get_product_details(product_soup)
            for key, value in product_details.items():
                if key not in data:
                    data[key] = [""] * len(data["title"])
                data[key].append(value)

            # Ensure every product detail column has a value for each row
            for key in data.keys():
                if len(data[key]) < len(data['title']):
                    data[key].append("")

# Convert the collected data into a DataFrame and save it as a CSV file
df = pd.DataFrame.from_dict(data)
df.to_csv('ankurL2.csv', index=False, encoding='utf-8-sig')
