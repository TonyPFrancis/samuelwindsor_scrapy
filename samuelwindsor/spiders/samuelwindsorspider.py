__author__ = 'tony'
from scrapy import Spider
from scrapy.http import Request
from scrapy.shell import inspect_response


class SamuelWindsorSpider(Spider):

    name = "samuelwindsorspider"
    allwed_domains = [
        'samuel-windsor.co.u',
    ]

    start_urls = [
        'http://www.samuel-windsor.co.uk/'
    ]

    # base_url of spider

    # variable to store main_categories
    main_categories = []
    sub_categories = {}

    def parse(self, response):
        '''
        function to fetch category
        :param response:
        :return:
        '''

        print ">>>>>>>>>>"
        print "MAIN URL"
        print response.url

        # fetching main_categories_selector
        main_categories_selector = response.xpath(
            "//div[@id=\"menu\"]/ul/li[not(contains(@class,\"showInMobile\") or contains(@class,\"clearance\"))]")
        print ">>>>>>>>>>"
        print "MAIN CATEGORIES SELECTOR"
        print main_categories_selector

        # fetching main_categories
        self.main_categories = response.xpath(
            "//div[@id=\"menu\"]/ul/li[not(contains(@class,\"showInMobile\") or contains(@class,\"clearance\"))]/a/text()").extract()
        print ">>>>>>>>>>"
        print "MAIN CATEGORIES"
        print self.main_categories

        # fetching sub_categories
        for x in main_categories_selector:
            self.sub_categories[
                str(x.xpath("a/text()").extract()[0])] = x.xpath("div/div/a/text()").extract()
        print ">>>>>>>>>>"
        print "SUBCATRGORIES"
        print self.sub_categories

        # fetching sub_categories_selector
        sub_categories_selector = {}
        for x in main_categories_selector:
            sub_categories_selector[
                str(x.xpath("a/text()").extract()[0])] = x.xpath("div/div/a/@href").extract()
        print ">>>>>>>>>>"
        print "SUBCATRGORIES SELECTOR"
        print sub_categories_selector

        # parse category webpages with parse_category
        for x in sub_categories_selector.keys():
            if sub_categories_selector[x]:
                for y in sub_categories_selector[x]:
                    yield Request(url=y, callback=self.parse_category)

    def parse_category(selfself, response):
        '''
        function to fetch products from categories
        :param selfself:
        :param response:
        :return:
        '''

        print ">>>>>>>>>>"
        print "CATGORY URL"
        print response.url
        inspect_response(response)
