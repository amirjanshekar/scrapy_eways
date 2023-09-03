import scrapy
import json
import http.client
import os


def change_price(price):
    if price < 5000000:
        return price + price * 5 / 100
    elif price < 10000000:
        return price + price * 4 / 100
    elif price < 20000000:
        return price + price * 3 / 100
    else:
        return price + price * 2 / 100


class EwaysSpider(scrapy.Spider):
    name = "eways"
    allowed_domains = ["panel.eways.ir"]
    start_urls = reversed([
        "https://panel.eways.co/store/list/16777/2/2/0/0/0/10000000000/",
        "https://panel.eways.co/store/list/16777/2/2/1/0/0/10000000000/",
        "https://panel.eways.co/store/list/14548/2/2/0/0/0/10000000000/",
        "https://panel.eways.co/store/list/17132/2/2/0/0/0/10000000000/",
        "https://panel.eways.co/store/list/14175/2/2/0/0/0/10000000000/",
        "https://panel.eways.co/store/list/1593/2/2/0/0/0/10000000000/",
        "https://panel.eways.co/Store/List/16778/2/2/0/0/0/10000000000",
        "https://panel.eways.co/store/list/2556/2/2/0/0/0/10000000000/"
    ])
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic '
                         'Y2tfOWE1Mjg3Yzg1NDIzMjczYWQ2MTdiMjk4Mjc0OWE1ZjBiNjJhZjM5OTpjc1'
                         '84NWNhNDk5NDU1OWJhY2Y2NGIyMTY2ZGQ1ODViNmFhZWY4YzU3N2Rm'
    }

    def parse(self, response):
        names = response.xpath('//*[@class="goods-record-title"]/text()').extract()
        prices = response.xpath('//*[@class="goods-record-price"]/text()').extract()
        if os.path.isfile(f"./scrap_eways/files/eways_{response.request.url.split('/')[5]}_"
                          f"{response.request.url.split('/')[8]}.json"):
            with open(
                    f"./scrap_eways/files/eways_{response.request.url.split('/')[5]}_"
                    f"{response.request.url.split('/')[8]}.json", "r+") as jsonFile:
                data = json.load(jsonFile)
                for i in range(min(len(names), len(prices))):
                    if prices[i] != "##price##":
                        try:
                            if str(round(change_price(int("".join(prices[i].split(","))) / 10))) != data[names[i]]["price"]:
                                payload = json.dumps({
                                    "name": names[i],
                                    "regular_price": str(round(change_price(int("".join(prices[i].split(","))) / 10))),
                                })
                                update_id = data[names[i]]["id"]
                                conn = http.client.HTTPSConnection("alidombe.com")
                                conn.request("PUT", f"/wp-json/wc/v3/products/{update_id}", payload, self.headers)
                                res = conn.getresponse()
                                data3 = json.loads(res.read().decode())
                                data[names[i]] = {
                                    "price": str(round(change_price(int("".join(prices[i].split(","))) / 10))),
                                    "id": data3['id'],
                                    "permalink": data3['permalink'],
                                    "site": response.request.url.split('/')[2]
                                }

                        except KeyError:
                            payload = json.dumps({
                                "name": names[i],
                                "regular_price": str(round(change_price(int("".join(prices[i].split(","))) / 10))),
                                "type": "simple",
                            })
                            conn = http.client.HTTPSConnection("alidombe.com")
                            conn.request("POST", "/wp-json/wc/v3/products", payload, self.headers)
                            res = conn.getresponse()
                            data2 = json.loads(res.read().decode())
                            data[names[i]] = {
                                "price": str(round(change_price(int("".join(prices[i].split(","))) / 10))),
                                "id": data2['id'],
                                "permalink": data2['permalink'],
                                "site": response.request.url.split('/')[2]
                            }
                jsonFile.seek(0)
                json.dump(data, jsonFile, indent=4)
                jsonFile.truncate()
        else:
            with open(
                    f"./scrap_eways/files/eways_{response.request.url.split('/')[5]}_"
                    f"{response.request.url.split('/')[8]}.json",
                    'a+') as jsonFile:
                item_dict = {}
                for i in range(min(len(names), len(prices))):
                    if prices[i] != "##price##":
                        payload = json.dumps({
                            "name": names[i],
                            "regular_price": str(round(change_price(int("".join(prices[i].split(","))) / 10))),
                            "type": "simple",
                        })
                        conn = http.client.HTTPSConnection("alidombe.com")
                        conn.request("POST", "/wp-json/wc/v3/products", payload, self.headers)
                        res = conn.getresponse()
                        data3 = json.loads(res.read().decode())
                        item_dict[names[i]] = {
                            "price": str(round(change_price(int("".join(prices[i].split(","))) / 10))),
                            "id": data3["id"],
                            "permalink": data3['permalink'],
                            "site": response.request.url.split('/')[2]
                        }
                json_string = json.dumps(item_dict)
                jsonFile.write(json_string)
