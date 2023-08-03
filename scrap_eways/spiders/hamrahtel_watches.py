import scrapy
import csv


class HamrahtelWatchesSpider(scrapy.Spider):
    name = "hamrahtel_watches"
    allowed_domains = ["hamrahtel.com"]
    start_urls = ["https://hamrahtel.com/list/llp-23/%D8%B3%D8%A7%D8%B9%D8%AA-%D9%88-%D9%85%DA%86-%D8%A8%D9%86%D8%AF-%D9%87%D9%88%D8%B4%D9%85%D9%86%D8%AF"]

    def parse(self, response):
        names = response.xpath(
            '//*[@class="text-sm font-normal items-center text-center m-auto line-clamp-2 "]/text()').extract()
        prices = response.xpath('//*[@class="price actual-price flex items-center text-md font-bold '
                                'text-red-400"]/text()').extract()
        for item in names:
            print(item)
        with open("./scrap_eways/files/hamrahtel_watches.csv", 'w+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['name', 'price'])
            for i in range(len(names)):
                csvwriter.writerow([names[i], prices[i]])
