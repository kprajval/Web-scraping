from bs4 import BeautifulSoup
import pandas as pd
import requests

prices = []
prod_name = []
rating = []
no_of_review = []
prod_url = []

for i in range(1, 20):
    URL = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1697538447&sprefix=ba%2Caps%2C283&ref=sr_pg_{i}'
    HEADER = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
               'Accept-Language': 'en-US, en;q=0.5'})

    webpage = requests.get(URL, headers=HEADER)
    soup = BeautifulSoup(webpage.content, 'html.parser')

    all_prod = soup.find_all("div", attrs={'data-component-type': 's-search-result'})

    for prod in all_prod:
        product_link = prod.find("a", class_="a-link-normal s-no-outline")
        if product_link:
            new_url = 'https://www.amazon.in' + product_link['href']
            prod_url.append(new_url)

            new_webpage = requests.get(new_url, headers=HEADER)
            new_soup = BeautifulSoup(new_webpage.content, 'html.parser')

            product_title = new_soup.find("span", id="productTitle")
            if product_title:
                prod_name.append(product_title.get_text().strip())

            product_price = new_soup.find("span", class_="a-price-whole")
            if product_price:
                prices.append(product_price.get_text())

            product_rating = new_soup.find("span", class_="a-icon-alt")
            if product_rating:
                rating.append(product_rating.get_text())

            review_count = new_soup.find("span", id="acrCustomerReviewText")
            if review_count:
                no_of_review.append(review_count.get_text())

            new_webpage.close()

data = {'Product URL': prod_url, 'Product Name': prod_name, 'Price': prices, 'Rating': rating, 'Number of Reviews': no_of_review}
df = pd.DataFrame(data)

path = r"C:\Users\Prajval\Desktop\data.csv"
df.to_csv(path, index=False)