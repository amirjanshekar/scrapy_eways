import scrapy
import csv


class Eways2Spider(scrapy.Spider):
    name = "eways2"
    allowed_domains = ["panel.eways.ir"]
    start_urls = ["https://panel.eways.co/store/list/14548/2/2/0/0/0/10000000000/"]

    def parse(self, response):
        names = response.xpath('//*[@class="goods-record-title"]/text()').extract()
        prices = response.xpath('//*[@class="goods-record-price"]/text()').extract()
        with open("./scrap_eways/files/eways_watches.csv", 'w+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['name', 'price'])
            for i in range(len(names)):
                csvwriter.writerow([names[i], prices[i]])
