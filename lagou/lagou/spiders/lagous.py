# -*- coding: utf-8 -*-
import scrapy
import time
import random
from lxml import etree
from selenium import webdriver


class LagousSpider(scrapy.Spider):
    name = 'lagous'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/jobs/list_python']

    driver = webdriver.Chrome()
    all_links = []

    # def process_request(self, request, spider):
    #     if spider.name == 'lagous':
    #         self.driver.get(request.url)
    #         time.sleep(3)
    #         body = self.driver.page_source
    def detail_links(self,source):
        detail_links = source.xpath('//a[@class="position_link"]/@href').extract()
        for detail_link in detail_links:
            yield scrapy.Request(url=detail_link,
                          callback=self.parse_detail)

    def parse(self, response):
        #print(response.text)
        self.driver.get(response.url)
        # 用于记录当前是第几页
        count_page = 1
        # 循环翻页直到最后一页
        while True:
            # 获取当前页的网页源代码
            source = self.driver.page_source
            # 利用xpath解析source获得detail_links并保存到
            #self.detail_links(source)
            source = etree.HTML(source)
            detail_links = source.xpath('//a[@class="position_link"]/@href')
            for detail_link in detail_links:
                yield scrapy.Request(url=detail_link,
                                     callback=self.parse_detail)
            print('Fetched page %s.' % str(count_page))
            time.sleep(3)
            try:
                bug=self.driver.find_element_by_xpath('//div[@class="body-btn"]')
                bug.click()
            except:
                print("探矿清楚")
            time.sleep(1)
            # 找到【下一页】按钮所在的节点
            next_btn = self.driver.find_element_by_xpath('//div[@class="pager_container"]/span[@class="pager_next "]')
            # 判断【下一页】按钮是否可用
            if "pager_next pager_next_disabled" in next_btn.get_attribute("class"):
                # 【下一页】按钮不可用时即达到末页，退出浏览器
                self.driver.quit()
                # 返回所有职位详情页url列表（去重后的）
                # return list(set(self.all_links))
            else:
                # 【下一页】按钮可用则点击翻页
                next_btn.click()
                count_page += 1
            #     time.sleep(random.randint(2, 4))
            # time.sleep(random.randint(3, 5))

        #job_city= response.xpath("//*[@class='job_request']/p/span[2]/text()").extract()


    def parse_detail(self,response):
        #解析详情页，用xpath提取出需要保存的职位详情信息并保存
        #对html用xpath语法找到职位名称所在节点的文本，即position_name
        position_name = response.xpath("//span[@class='name']/text()").extract_first()
        # 对html用xpath语法找到职位id所在的节点，提取获得position_id
        #position_id = response.xpath("//link[@rel='canonical']/@href").extract_first().split('/')[-1].replace('.html', '')

        # 找到职位标签，依次获取：薪资、城市、年限、受教育程度、全职or兼职
        job_request_spans = response.xpath('//dd[@class="job_request"]')
        salary = job_request_spans.xpath('.//span[1]/text()').extract_first().strip()  # 列表索引0==xpath第1个节点
        city = job_request_spans.xpath('.//span[2]/text()').extract_first().strip().replace("/", "").strip()
        work_year = job_request_spans.xpath('.//span[3]/text()').extract_first().strip("/").strip()
        education = job_request_spans.xpath('.//span[4]/text()').extract_first().strip("/").strip()

        #找到公司标签，获取company_short_name
        company_short_name = response.xpath('//dl[@class="job_company"]//em/text()').extract_first().replace("\n", "").strip()
        # 找到公司标签中的industry_field和finance_stage
        company_infos = response.xpath('//dl[@class="job_company"]//li')  # 注意该节点下的text()索引0和2是空的
        industry_field = company_infos.xpath('./h4/text()').extract_first().replace("\n", "").strip()
        finance_stage = company_infos[1].xpath('./h4/text()').extract_first().replace("\n", "").strip()

        # 找到工作地址所在的区
        district = response.xpath('//div[@class="work_addr"]/a[2]/text()').extract_first().strip()

        # 找到职位诱惑，获取position_advantage
        position_advantage = response.xpath('//dd[@class="job-advantage"]//p/text()').extract_first().strip("/").strip()
        print(position_advantage)
        # # 找到所有职位标签，用","连接成字符串
        # position_labels = ",".join(response.xpath('//li[@class="labels"]//text()').extract()).strip()






