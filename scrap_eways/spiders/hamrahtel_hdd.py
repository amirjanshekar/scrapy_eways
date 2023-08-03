import scrapy
import csv


class HamrahtelHddSpider(scrapy.Spider):
    name = "hamrahtel_hdd"
    allowed_domains = ["hamrahtel.com"]
    start_urls = ["https://hamrahtel.com/list/llp-136/%D9%87%D8%A7%D8%B1%D8%AF-%D8%A7%DA%A9%D8%B3%D8%AA%D8%B1%D9%86"
                  "%D8%A7%D9%84"]

    def parse(self, response):
        names = response.xpath(
            '//*[@class="text-sm font-normal items-center text-center m-auto line-clamp-2 "]/text()').extract()
        prices = response.xpath('//*[@class="price actual-price flex items-center text-md font-bold '
                                'text-red-400"]/text()').extract()
        for item in names:
            print(item)
        with open("./scrap_eways/files/hamrahtel_hdd.csv", 'w+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['name', 'price'])
            for i in range(len(names)):
                csvwriter.writerow([names[i], prices[i]])
