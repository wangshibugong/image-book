from scrapy import cmdline
#cmdline.execute("scrapy crawl book -o jd.jsonlines -s FEED_EXPORT_ENCODING=UTF-8".split())
cmdline.execute("scrapy crawl weibo_spider ".split())

