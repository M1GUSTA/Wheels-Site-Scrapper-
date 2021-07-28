import json
import os
import re

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


def get_data(url):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Is-Ajax-Request": "X-Is-Ajax-Request",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/92.0.4515.107 Safari/537.36 "
    }
    current_date = datetime.now().strftime("%d_%m_%Y %H_%M")
    r = requests.get(url, headers=headers)

    # with open("r.json", 'w', encoding="utf-8") as file:
    #         json.dump(r.json(), file, indent=4, ensure_ascii=False)

    pages_count = r.json()["pageCount"]

    data_list = []
    for page in range(1, pages_count + 1):
        url = url + f"&PAGEN_1={page}"

        r = requests.get(url=url, headers=headers)
        data = r.json()
        items = data["items"]

        possidble_stores = ["discountStores", "fortochkiStores", "commonStores"]
        for item in items:
            total_amount = 0

            item_name = item["name"]
            item_price = item["price"]
            item_img = f"https://roscarservis.ru{item['imgSrc']}"
            item_url = f"https://roscarservis.ru{item['url']}"

            stores = []
            for ps in possidble_stores:
                if ps in item:
                    if item[ps] is None or len(item[ps]) < 1:
                        continue
                    else:
                        for store in item[ps]:
                            store_name = store['STORE_NAME']
                            store_price = store["PRICE"]
                            store_amount = store['AMOUNT']
                            total_amount += int(store["AMOUNT"])

                            stores.append(
                                {
                                    "store_name": store_name,
                                    "store_price": store_price,
                                    "store_amount": store_amount
                                }
                            )
            data_list.append(
                {
                    "name": item_name,
                    "price": item_price,
                    "url": item_url,
                    "img_url": item_img,
                    "total_amount": total_amount
                }
            )
        print(f"[INFO] Обработал {page}/{pages_count}")
    with open(f"file_{current_date}.json", "a") as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)

def main():
    get_data("https://roscarservis.ru/catalog/legkovye/?form_id=catalog_filter_form&filter_mode=params&sort=asc"
             "&filter_type=tires&arCatalogFilter_458_1500340406=Y&set_filter=Y&arCatalogFilter_463=668736523")


if __name__ == '__main__':
    main()
