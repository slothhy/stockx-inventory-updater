import requests
import os
from openpyxl import load_workbook
from forex_python.converter import CurrencyRates
from datetime import datetime
import json
import time

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def load_config():
    with open(os.path.join(__location__, "config.json")) as json_file:
        data = json.load(json_file)
        return data

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # pylint: disable=no-member
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def main():
    config = load_config()
   
    if config["currency"] == "USD":
        rate = 1 
    else:
        c = CurrencyRates()
        rate = c.get_rate('USD', config["currency"])

    wb = load_workbook(resource_path("./stockx_book.xlsx"))
    ws = wb['Sheet1']

    session = requests.Session()
    session.headers.update({
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'accept': '*/*',
        'accept-ending': 'gzip, deflate, br',
        'connection': 'keep-alive'
    })
    # session.get("https://stockx.com/api/browse?&_search=EF2367&dataType=product")
    # print(session.cookies)

    row_num = config["start-row"]

    for row in ws.iter_rows(min_row=config["start-row"]): 
        if row[0].value == None:
            break
        print(f'Fetching row {row_num}: {row[0].value}')
        urlkey = search_product(row[0].value, session)
        if urlkey is None:
            break
        row[6].value = "Stockx"
        row[6].hyperlink = f'https://stockx.com/{urlkey}'
        result = product_info(urlkey, str(row[2].value), session)
        if result is None:
            break
        row[1].value = result["title"]
        if result["uuid"] is None:
            print("Size not found, check if W or Y is needed.")
            break
        sales = get_sales(result["uuid"], session)
        row[4].value = round((sales["last"] * rate), 2)
        row[5].value = round((sales["average"] * rate), 2)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %I:%M:%S %p")
        row[7].value = dt_string
        row_num += 1
        
    wb.save(resource_path("./stockx_book_output.xlsx"))

def search_product(sku, session):
    url = f'https://stockx.com/api/browse?&_search={sku}&dataType=product'
    # headers = {
    #     'content-type': 'application/x-www-form-urlencoded',
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    #     'accept': '*/*',
    #     'accept-ending': 'gzip, deflate, br',
    #     'connection': 'keep-alive'
    # }
    req = session.get(url)
    if req.status_code == 200:
        data = req.json()
        urlkey = data["Products"][0]["urlKey"]
        return urlkey
    else:
        print(f'Error {req.status_code} search_product')
    
def product_info(urlkey, size, session):
    url = f'https://stockx.com/api/products/{urlkey}?includes=market&currency=USD'
    # headers = {
    #     'content-type': 'application/x-www-form-urlencoded',
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    #     'accept': '*/*',
    #     'accept-ending': 'gzip, deflate, br',
    #     'connection': 'keep-alive'
    # }
    req = session.get(url)
    if req.status_code == 200:
        data = req.json()
        result = {}
        result["title"] = data["Product"]["title"]
        result["uuid"] = None
        for key in data["Product"]["children"]:
            if (data["Product"]["children"][key]["shoeSize"]) == size:
                uuid = data["Product"]["children"][key]["uuid"]
                result["uuid"] = uuid
                break
        return result
    else:
        print(f'Error {req.status_code} product_info')

def get_sales(uuid, session):
    url = f'https://stockx.com/api/products/{uuid}/activity?state=480&currency=USD&limit=3&page=1&sort=createdAt&order=DESC'
    # headers = {
    #     'content-type': 'application/x-www-form-urlencoded',
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    #     'accept': '*/*',
    #     'accept-ending': 'gzip, deflate, br',
    #     'connection': 'keep-alive'
    # }
    req = session.get(url)
    if req.status_code == 200:
        data = req.json()
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
    else:
        print(f'Error {req.status_code} get_sales')
    
if __name__ == '__main__':
    main()