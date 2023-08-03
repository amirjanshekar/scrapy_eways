import scrapy
import csv


class HamrahtelHeadphonesSpider(scrapy.Spider):
    name = "hamrahtel_headphones"
    allowed_domains = ["hamrahtel.com"]
    start_urls = ["https://hamrahtel.com/list/llp-84/%D9%87%D8%AF%D9%81%D9%88%D9%86-%D9%88-%D9%87%D9%86%D8%AF%D8%B2%D9%81%D8%B1%DB%8C"]

    def parse(self, response):
        names = response.xpath(
            '//*[@class="text-sm font-normal items-center text-center m-auto line-clamp-2 "]/text()').extract()
        prices = response.xpath('//*[@class="price actual-price flex items-center text-md font-bold '
                                'text-red-400"]/text()').extract()
        for item in names:
            print(item)
        with open("./scrap_eways/files/hamrahtel_headphones.csv", 'w+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['name', 'price'])
            for i in range(len(names)):
                csvwriter.writerow([names[i], prices[i]])
