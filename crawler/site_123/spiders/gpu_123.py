import scrapy
import numpy as np
from scrapy.crawler import CrawlerProcess
from datetime import date

def errors(request):
    if len(request) > 0:
        return request[0].split('>')[1].split('<')[0]
    else:
        return np.nan
def ram_error(request):
    if len(request) > 0:
        return request[0].split('-')[2].split('mb')[0]
    else:
        return np.nan

class Gpu123Spider(scrapy.Spider):

    name = 'gpu_123'
    start_urls = ['https://www.123.ru/komplektuyuschie_dlya_pk/videokarti/']
    
    def parse(self, response):

        for link in response.xpath("//*[@id='products-list']/div/div[3]/div/a[@href[1]]").extract():
            yield response.follow(link.split('"')[1][36::], callback=self.parse_pages)
        for i in range(2, 15):
            next_page = 'https://www.123.ru/komplektuyuschie_dlya_pk/videokarti/page-'+str(i)
            yield response.follow(next_page, callback=self.parse)
    
    def parse_pages(self, response):
        yield {
                'title': response.xpath('//*[@id="body"]/section[3]/div[2]/div[2]/h1/text()').extract()[0].replace('Видеокарта ', ''),
                'price': int(response.xpath('//*[@id="body"]/section[3]/div[2]/div[3]/div[2]/div[1]/div[1]/span[1]/div/text()').extract()[0].replace(' ', '')),
                'brand': errors(response.xpath('//*[@id="tab-char"]/div[1]/aside/div/div[1]/span').extract()),
                'Model': errors(response.xpath('//*[@id="tab-char"]/div[1]/aside/div/div[6]/span').extract()),
                'frequency': errors(response.xpath('//*[@id="tab-char"]/div[1]/aside/div/div[7]/span').extract()),
                'RAM' : ram_error(response.css('#tab-char > div.content-wrp.properties-source > aside > div > div:nth-child(9) > span > a').extract())
            }
process = CrawlerProcess(settings={
    "FEEDS": {
        f"gpu_{date.today()}.csv": {"format": "csv"},
    },
})
process.crawl(Gpu123Spider)
process.start()