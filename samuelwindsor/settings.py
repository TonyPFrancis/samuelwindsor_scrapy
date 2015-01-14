# -*- coding: utf-8 -*-

# Scrapy settings for samuelwindsor project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
from scrapy.settings.default_settings import ITEM_PIPELINES


BOT_NAME = 'samuelwindsorspider'

SPIDER_MODULES = ['samuelwindsor.spiders']
NEWSPIDER_MODULE = 'samuelwindsor.spiders'

ITEM_PIPELINES = {
    'samuelwindsor.pipelines.SamuelwindsorPipeline': 1,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'samuelwindsor (+http://www.yourdomain.com)'
