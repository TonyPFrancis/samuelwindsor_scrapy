
__author__ = 'tony'
from scrapy import Spider
from scrapy.http import Request
from scrapy.shell import inspect_response
from samuelwindsor.items import SamuelwindsorItem
import re
from datetime import datetime
from slugify import slugify


class SamuelWindsorSpider(Spider):

    name = "samuelwindsorspider"
    allwed_domains = [
        'samuel-windsor.co.u',
    ]

    start_urls = [
        'http://www.samuel-windsor.co.uk/'
    ]

    # base_url of spider
    base_url = 'http://www.samuel-windsor.co.uk/'

    # variable to store main_categories
    main_categories = []
    sub_categories = {}

    # current runtime of spider
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # total product count
    total_product = 0

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

    def parse_category(self, response):
        '''
        function to fetch products from categories
        :param selfself:
        :param response:
        :return:
        '''

        print ">>>>>>>>>>"
        print "CATGORY URL"
        print response.url

        # fetching products from category
        product_urls = response.xpath(
            "//div[@class=\"prodbox\"]/a/@href").extract()
        # requesting for products urls
        if product_urls:
            for x in product_urls:
                yield Request(url=self.base_url + x, callback=self.parse_product)

    def parse_product(self, response):
        '''
        function to parse products
        :param response:
        :return:
        '''

        print ">>>>>>>>>>"
        print "PRODUCT URL"
        print response.url

        # item of SamuelwindsorItem
        item = SamuelwindsorItem()

        # fetching crawl_date
        item['crawl_date'] = self.current_time

        # fetching id
        item['id'] = response.url

        # fetching product_description
        product_description = response.xpath(
            "//div[@id=\"description\"]//text()").extract()
        product_description = ". ".join(
            [x.strip() for x in product_description if x.strip()])
        item['product_description'] = product_description

        # fetching product_id
        product_id = response.xpath(
            "//p[@class=\"prodcode\"]/text()").extract()[0]
        product_id = product_id.rstrip('-')
        product_id = re.split(r'\s*:?', product_id)[-1]
        item['product_id'] = product_id

        # fetching price
        price = response.xpath(
            "//p[@class=\"prodOffer\"]//text()").extract()[0]
        price = float(price.encode('ascii', 'ignore').strip())
        item['price'] = price

        # fetching size
        size = response.xpath(
            "//select[@name=\"SKURecNum\"]/option/text()").extract()[1:]
        size = [x.strip().split('-')[0].strip() for x in size]
        item['size'] = size

        # fetching product_name
        product_name = response.xpath(
            "//h1[@class=\"prodTitle\"]/text()").extract()[0]
        item['product_name'] = product_name

        # fetching product_title_slug
        item['product_title_slug'] = slugify(product_name)

        # fetching product_img
        product_img = response.xpath(
            "//div[@id=\"thumbs\"]/ul/li/a/img/@src").extract()
        product_img = [self.base_url + x for x in product_img]
        # changing images to higher resolution
        product_img = [
            "products/optimised/".join(x.split("tinythumbs/thumb-")) for x in product_img]
        item['product_img'] = product_img

        # fetching country
        country = "United Kingdom"
        item['country'] = country

        # fetching country_slug
        item['country_slug'] = slugify(country)

        # fetching source_text
        item['source_text'] = "samuel_windsor_uk"

        # fetching shop_slug
        item['shop_slug'] = slugify("samuel_windsor_uk")

        # fetching product_brand
        product_brand = "SAMUEL WINDSOR"
        item['product_brand'] = product_brand

        # fetching brand_slug
        item['brand_slug'] = slugify(product_brand)

        # fetching category
        sub_category = response.xpath(
            "//span[@itemprop=\"title\"]/text()").extract()[0]
        main_category = None
        for k, v in self.sub_categories.items():
            if sub_category in v:
                main_category = k
                break

        if main_category == None:
            sub_category = None

        # assigning main_category
        item['main_category'] = main_category

        # assigning category_slug
        if main_category:
            item['category_slug'] = slugify(main_category)
        else:
            item['category_slug'] = None

        # assigning product_category
        item['product_category'] = sub_category

        # assigning subcategory_slug
        if sub_category:
            item['subcategory_slug'] = slugify(sub_category)
        else:
            item['subcategory_slug'] = None

        print ">>>>>>>>>>"
        print "TOTAL PRODUCT"
        self.total_product += 1
        print self.total_product
        print ">>>>>>>>>>"
        print "ITEM"
        print item
        yield item

