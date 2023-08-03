import scrapy
import csv


class EwaysSpider(scrapy.Spider):
    name = "eways"
    allowed_domains = ["panel.eways.ir"]
    start_urls = ["https://panel.eways.ir/store/categorylist/4285/"]

    def parse(self, response):
        names = response.xpath('//*[@class="goods-item-title mt-2"]/a/span/text()').extract()
        prices = response.xpath('//*[@class="price"]/text()').extract()
        with open("./scrap_eways/files/eways_phones.csv", 'w+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['name', 'price'])
            for i in range(len(names)):
                csvwriter.writerow([names[i], prices[i]])
