import scrapy


class HamrahtelPhoneSpider(scrapy.Spider):
    name = "hamrahtel_phone"
    allowed_domains = ["hamrahtel.com"]
    start_urls = ["https://hamrahtel.com/list/llp-20/%DA%AF%D9%88%D8%B4%DB%8C-%D9%85%D9%88%D8%A8%D8%A7%DB%8C%D9%84-2"]

    def parse(self, response):
        pass
