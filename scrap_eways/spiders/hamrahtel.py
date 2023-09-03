import scrapy
import json
import os
import http.client


def change_price(price):
    if price < 5000000:
        return price + price * 5 / 100
    elif price < 10000000:
        return price + price * 4 / 100
    elif price < 20000000:
        return price + price * 3 / 100
    else:
        return price + price * 2 / 100


class HamrahtelSpider(scrapy.Spider):
    name = "hamrahtel"
    allowed_domains = ["hamrahtel.com"]
    start_urls = ["https://app.hamrahtel.com/api/categories/20/products/?In_Stock_Only=true&page=2",
                  "https://app.hamrahtel.com/api/categories/20/products/?In_Stock_Only=true",
                  "https://app.hamrahtel.com/api/categories/130/products/?In_Stock_Only=true",
                  "https://app.hamrahtel.com/api/categories/23/products/?In_Stock_Only=true",
                  "https://app.hamrahtel.com/api/categories/84/products/?In_Stock_Only=true",
                  "https://app.hamrahtel.com/api/categories/85/products/?In_Stock_Only=true"]
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic '
                         'Y2tfOWE1Mjg3Yzg1NDIzMjczYWQ2MTdiMjk4Mjc0OWE1ZjBiNjJhZjM5OTpjc1'
                         '84NWNhNDk5NDU1OWJhY2Y2NGIyMTY2ZGQ1ODViNmFhZWY4YzU3N2Rm'
    }

    def parse(self, response):
        json_res = json.loads(response.body)
        products = json_res["products"]
        url = response.request.url
        if os.path.isfile(f"./scrap_eways/files/hamrahtel_{url.split('/')[5].split('.')[0]}.json"):
            with open(
                    f"./scrap_eways/files/hamrahtel_{url.split('/')[5].split('.')[0]}"
                    f".json", "r+") as jsonFile:
                data = json.load(jsonFile)
                for item in products:
                    try:
                        if str(round(item['price'])) != data[item['name']]["price"]:
                            payload = json.dumps({
                                "name": item['name'],
                                "regular_price": str(round(change_price(item['price']))),
                            })
                            update_id = data[item['name']]["id"]
                            conn = http.client.HTTPSConnection("alidombe.com")
                            conn.request("PUT", f"/wp-json/wc/v3/products/{update_id}", payload, self.headers)
                            res = conn.getresponse()
                            data3 = json.loads(res.read().decode())
                            data[item['name']] = {
                                "price": str(round(change_price(item['price']))),
                                "id": data3['id'],
                                "permalink": data3['permalink'],
                                "site": url.split('/')[2]
                            }
                    except KeyError:
                        payload = json.dumps({
                            "name": item['name'],
                            "regular_price": str(round(change_price(item['price']))),
                            "type": "simple",
                        })
                        conn = http.client.HTTPSConnection("alidombe.com")
                        conn.request("POST", "/wp-json/wc/v3/products", payload, self.headers)
                        res = conn.getresponse()
                        data2 = json.loads(res.read().decode())
                        data[item['name']] = {
                            "price": str(round(change_price(item['price']))),
                            "id": data2['id'],
                            "permalink": data2['permalink'],
                            "site": url.split('/')[2]
                        }
                jsonFile.seek(0)
                json.dump(data, jsonFile, indent=4)
                jsonFile.truncate()
        else:
            with open(
                    f"./scrap_eways/files/hamrahtel_{url.split('/')[5].split('.')[0]}"
                    f".json", 'a+') as jsonFile:
                item_dict = {}
                for element in products:
                    payload = json.dumps({
                        "name": element['name'],
                        "regular_price": str(round(change_price(element['price']))),
                        "type": "simple",
                    })
                    conn = http.client.HTTPSConnection("alidombe.com")
                    conn.request("POST", "/wp-json/wc/v3/products", payload, self.headers)
                    res = conn.getresponse()
                    data3 = json.loads(res.read().decode())
                    item_dict[element['name']] = {
                        "price": str(round(change_price(element['price']))),
                        "id": data3["id"],
                        "permalink": data3['permalink'],
                        "site": url.split('/')[2]
                    }
                json_string = json.dumps(item_dict)
                jsonFile.write(json_string)
