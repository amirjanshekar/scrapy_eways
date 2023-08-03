import scrapy
import csv


class EwaysLaptopSpider(scrapy.Spider):
    name = "eways_laptop"
    allowed_domains = ["panel.eways.ir"]
    start_urls = ["https://panel.eways.ir/Store/List/16778/2/2/0/0/0/10000000000"]

    def parse(self, response):
        names = response.xpath('//*[@class="goods-record-title"]/text()').extract()
        prices = response.xpath('//*[@class="goods-record-price"]/text()').extract()
        with open("./scrap_eways/files/eways_laptop.csv", 'w+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['name', 'price'])
            for i in range(len(names)):
                if prices[i] != "##price##":
                    csvwriter.writerow([names[i], prices[i]])

