import scrapy
import csv


class AasoodHddSpider(scrapy.Spider):
    name = "aasood_hdd"
    allowed_domains = ["aasood.com"]
    start_urls = ["https://aasood.com/product-list/210020/Hard%20External"]

    def parse(self, response):
        names = response.xpath(
            '//*[@class="product-preview-fast-shopping_productPreviwLand__top__lgZWu"]/h3/text()').extract()
        prices = response.xpath('//*[@class="price-comp_priceComp__value__osMF2"]/span/text()').extract()
        links = response.xpath(
            '//*[@class="product-preview-fast-shopping_productPreviwLand__9TS3j"]/a/@href').extract()
        for item in prices:
            print(item)
        with open("./scrap_eways/files/aasood_hdd.csv", 'w+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['name', 'price', "link"])
            for i in range(len(names)):
                csvwriter.writerow([names[i], prices[i], links[i]])
