import requests
from bs4 import BeautifulSoup
from csv import writer
import webbrowser

def scrape(product, pageNum, toDo, params, dict, headerNames):
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = 'https://www.amazon.com/s?k=' + product + '&page=' + str(pageNum) + '&ref=nb_sb_noss_2'
    response = requests.get(url , headers=headers)
    soup = BeautifulSoup(response.content, features="lxml")
    print(url)

    print(soup)
    products = soup.findAll(class_='sg-col-inner')
    print(products)

    with open('amz-products.csv', toDo) as csv_file:
        csv_writer = writer(csv_file)
        headers = ['Name']
        for num in params:
            headers.append(headerNames[num])
        if (toDo == 'w'):
            csv_writer.writerow(headers)
        print('goes here')

        for product in products:
            print('here too')
            vals = []
            name = product.find(class_='a-size-base-plus a-color-base a-text-normal')
            if (name != None):
                name = name.get_text()
            elif (product.find(class_='a-size-medium a-color-base a-text-normal')):
                name = product.find(class_='a-size-medium a-color-base a-text-normal').get_text()
            else:
                continue
            vals.append(name)

            value = ''
            for num in params:
                value = product.find(class_ = dict[num])
                if (value != None):
                    if (num == 3):
                        value = True
                    else:
                        value = value.get_text()
                else:
                    if (num == 3):
                        value = False
                    else:
                        value = 'none' # CHANGE
                vals.append(value)
            print(vals)

            csv_writer.writerow(vals)

def getProduct(product):
    prod = product.strip()
    while len(prod) is 0:
        prod = input('What do you want to search for? ')
        prod = prod.strip()
    prod = prod.replace(" ", "+")
    return prod

def getParams():
    params = []
    print("Enter one number and press return | Enter 'done' when finished")
    while (True):
        param = input("What information would you like to see (enter number): \n1. Price   2. Rating   3. Prime   4. ALL   5. DONE\n").strip()
        if (param == "4" or param == "5"):
            if (param == "4"):
                params.append(1)
                params.append(2)
                params.append(3)
                break
            else:
                break
        elif (param != ""):
            if (int(param) not in params):
                params.append(int(param))
    return params

def run():
    dict = {1: 'a-offscreen', 2: 'a-icon-alt', 3: 'a-icon a-icon-prime a-icon-medium'}
    headerNames = {1: 'Price', 2: 'Rating', 3: 'Prime'}

    product = getProduct(input("What do you want to search for? "))
    params = getParams()
    numPages = input("How many pages do you want to search? ")

    scrape(product, 1, 'w', params, dict, headerNames) 
    for i in range(2, int(numPages) + 1):
        scrape(product, i, 'a', params, dict, headerNames)
    path = "/Users/asirohi/Documents/Python/web-scraping/amz-scraper/amz-products.csv"
    webbrowser.open('file:///' + path)

run()

# **FOR TESTING**
# **Enter values that you want to be searched as a list of strings in test
def test(list):
    # list[0] = getProduct(list[0])
    scrape(list[0], 1, 'w')
    for prod in list[1:]:
        # prod = getProduct(prod)
        scrape(prod, 1, 'a')
    path = "/Users/asirohi/Documents/Python/web-scraping/amz-scraper/amz-products.csv"
    webbrowser.open('file:///' + path)

# test(['phone case', 'pocket watch', '  christmas lights ', '   ', 'lamp', 'poster', 'barbie', 'barbed wire', 'fence', 'helmet'])