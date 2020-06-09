import requests
from bs4 import BeautifulSoup
from csv import writer
import webbrowser

def scrape(product, pageNum, toDo):
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    response = requests.get('https://www.amazon.com/s?k=' + product + '&page=' + str(pageNum) + '&ref=nb_sb_noss_2', headers=headers)
    soup = BeautifulSoup(response.content, features="lxml")

    products = soup.findAll(class_='a-section a-spacing-medium')

    with open('amz-products.csv', toDo) as csv_file:
        csv_writer = writer(csv_file)
        headers = ['Name', 'Price', 'Rating', 'Prime']
        if (toDo == 'w'):
            csv_writer.writerow(headers)

        for product in products:
            name = product.find(class_='a-size-base-plus a-color-base a-text-normal')
            if (name != None):
                name = name.get_text()
            elif (product.find(class_='a-size-medium a-color-base a-text-normal')):
                name = product.find(class_='a-size-medium a-color-base a-text-normal').get_text()
            else:
                name = 'none'
            price = product.find(class_='a-offscreen')
            if (price != None):
                price = price.get_text()
            else:
                price = 'none'
            rating = product.find(class_='a-icon-alt')
            if (rating != None):
                rating = rating.get_text()
            else:
                rating = 'none'
            prime = False
            if(product.find(class_='a-icon a-icon-prime a-icon-medium') != None):
                prime = True

            csv_writer.writerow([name, price, rating, prime])

def getProduct(product):
    prod = product.strip()
    while len(prod) is 0:
        prod = input('What do you want to search for? ')
        prod = prod.strip()
    prod = prod.replace(" ", "+")
    return prod

def run():
    product = getProduct(input("What do you want to search for? "))
    numPages = input("How many pages do you want to search? ")
    scrape(product, 1, 'w') 
    for i in range(2, int(numPages) + 1):
        scrape(product, i, 'a')
    path="/Users/asirohi/Documents/Python/Web Scraping/amz-products.csv"
    webbrowser.open('file:///' + path)

run()

# **FOR TESTING**
# **Enter values that you want to be searched as a list of strings in test
def test(list):
    scrape(list[0], 1, 'w')
    for prod in list[1:]:
        scrape(prod, 1, 'a')
    path="/Users/asirohi/Documents/Python/Web Scraping/amz-products.csv"
    webbrowser.open('file:///' + path)

# test(['test', 'test', 'test'])