import requests
import os
from openpyxl import load_workbook
from forex_python.converter import CurrencyRates
from datetime import datetime

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # pylint: disable=no-member
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def main():
    c = CurrencyRates()
    sgd_rate = c.get_rate('USD', 'SGD')

    wb = load_workbook(resource_path("./stockx_book.xlsx"))
    ws = wb['Sheet1']

    for row in ws.iter_rows(min_row=2): #start from row 2
        print(f'Doing {row[0].value}')
        urlkey = search_product(row[0].value)
        row[6].value = "Stockx"
        row[6].hyperlink = f'https://stockx.com/{urlkey}'
        result = product_info(urlkey, str(row[2].value))
        row[1].value = result["title"]
        if result["uuid"] == None:
            break
        sales = get_sales(result["uuid"])
        row[4].value = round((sales["last"] * sgd_rate), 2)
        row[5].value = round((sales["average"] * sgd_rate), 2)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %I:%M:%S %p")
        row[7].value = dt_string
        
    wb.save(resource_path("./stockx_book.xlsx"))

def search_product(sku):
    url = f'https://stockx.com/api/browse?&_search={sku}&dataType=product'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }
    data = requests.get(url, headers=headers).json()
    urlkey = data["Products"][0]["urlKey"]
    return urlkey
    
def product_info(urlkey, size):
    url = f'https://stockx.com/api/products/{urlkey}?includes=market&currency=USD'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }
    data = requests.get(url, headers=headers).json()
    result = {}
    result["title"] = data["Product"]["title"]
    result["uuid"] = None
    for key in data["Product"]["children"]:
        if (data["Product"]["children"][key]["shoeSize"]) == size:
            uuid = data["Product"]["children"][key]["uuid"]
            result["uuid"] = uuid
            break
    return result

def get_sales(uuid):
    url = f'https://stockx.com/api/products/{uuid}/activity?state=480&currency=USD&limit=3&page=1&sort=createdAt&order=DESC'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }
    data = requests.get(url, headers=headers).json()
    amount = 0
    limit = 0
    sales = {}
    for i in data["ProductActivity"]:
        if limit == 0:
            sales["last"] = i["localAmount"]
        amount += i["localAmount"]
        limit += 1
    average = amount / limit
    sales["average"] = round(average, 2)
    return sales
    
main()