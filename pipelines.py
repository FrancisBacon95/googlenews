# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
from GoogleNews.search_information import SearchInformation

class GooglenewsPipeline(object):
    
    def __init__(self):
        write_date=SearchInformation.str_from_date.replace(".","")
        self.file = open("from"+write_date+"_"+"GoogleNews.csv","wb")
        #  ,newline=""
        self.exporter = CsvItemExporter(self.file, encoding='utf-8',delimiter="-")
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item     
        
        '''   
    def process_item(self,item,spider):
        row=[]
        save_query=item['query'].replace(" ","+")
        row.append(save_query)
        row.append(item['title'])
        row.append(item['date'])
        row.append(item['publisher'])
        row.append(item['url'])
        row.append(item['content'])
        self.csvwriter.writerow(row)
        return item
        '''
        
        # cd Desktop/데이터몬스터즈/Project2/Scrapy_GoogleNews
        # scrapy crawl GoogleNewsCrawler