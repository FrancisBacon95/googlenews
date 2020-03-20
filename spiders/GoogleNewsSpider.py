# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 11:19:21 2019

@author: franc_000
"""
import scrapy
    
from GoogleNews.items import GNItem
from GoogleNews.search_information import SearchInformation
from newspaper import Article
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
    
class GoogleNewsSpider(scrapy.Spider) :
    name="GoogleNewsCrawler"
    allowed_domain=['google.com']
    
        
    def start_requests(self):        
            # search_information의 SearchInformation에서 넣어주었던 정보를 이용해서
            # 완성된 형태의 url을 만든다.
        url1 = 'https://www.google.com/search?q='        
        url2 = '&hl=en&source=lnt&tbs=cdr%3A1%2Ccd_min%3A'        
        url3 = '%2F'        
        url4 = '%2F'        
        url5 = '%2Ccd_max%3A'        
        url6 = '%2F'        
        url7 = '%2F'        
        url8 = '&tbm=nws'
        
        from_date=datetime.strptime(SearchInformation.str_from_date,"%Y.%m.%d")
        one_month=31
        edt_list=[]
        for one_day in range(0,one_month) :
            edt = from_date + relativedelta(days=one_day)
            edt_list.append(str(edt).split(" ")[0])
        
        for query in SearchInformation.query_list:
            for edt in edt_list:
                yy=edt.split('-')[0]
                mm=edt.split('-')[1]
                dd=edt.split('-')[2]
                
                url= url1 + query + url2 + mm + url3 + dd + url4 +yy + url5 + mm + url6 + dd + url7 +yy + url8
                yield scrapy.Request(url=url, callback=self.parse,headers={'Content-Type':'text/html; charset=UTF-8','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'})
                # user-agent를 default값으로 두면 기간설정 등이 안되는 오류가 발생한다.
                
    def parse(self, response):
                    
        item=GNItem()
        main_url="https://www.google.com"
        
                
        #한 덩어리 내 큰 기사 혹은 (뭉쳐있지 않고)하나만 있는 기사
        for i in range(1,len(response.xpath('//*[@id="rso"]/div/div'))+1):
            item['title']=' '.join(response.xpath('//*[@id="rso"]/div/div['+str(i)+']/div/div[1]/h3/a//text()').extract())
            article_url=response.xpath('//*[@id="rso"]/div/div['+str(i)+']/div/div[1]/h3/a/@href')[0].extract()
            item['url']=article_url
            item['publisher']=response.xpath('//*[@id="rso"]/div/div['+str(i)+']/div/div[1]/div[1]/span[1]/text()')[0].extract()
            item['query']=response.xpath('/html/head/title/text()')[0].extract().split(' - ')[0]
            
            article= Article(article_url,language='en')
            article.download()
            article.parse()
            
            
            date1=article.publish_date
            date2=str(response.xpath('//*[@id="tophf"]/input[@name="tbs"]/@value').extract()).split(',')[1].split(':')[1].replace('/','-')
            if date1 is not None :
                item['date']=date2  
                item['est_date']="True"
            else:
                item['date']=str(date1)
                item['est_date']="False"
            try :
                content=article.text
                item['content']=content

                # 주로 에러가 발생하면 시간초과 혹은 해당 사이트에서 크롤을 막았기 때문입니다.
            except :
                item['content']="ERROR2"
            

            yield item
                    
                    #한 덩어리 내 작은 기사(사진 하나에 최상단에는 큰 기사 하나가 있고 밑으로 딸려있는 기사들이 있는데 그것들을 작은 기사라고 칭함.)
            for j in range(2,len(response.xpath('//*[@id="rso"]/div/div['+str(i)+']/div/div'))+1,2):
                item['title']=' '.join(response.xpath('//*[@id="rso"]/div/div['+str(i)+']/div/div['+str(j)+']/a//text()').extract())
                article_url=response.xpath('//*[@id="rso"]/div/div['+str(i)+']/div/div['+str(j)+']/a/@href')[0].extract()
                item['url']=article_url
                item['publisher']=response.xpath('//*[@id="rso"]/div/div['+str(i)+']/div/div['+str(j)+']/span[1]/text()')[0].extract()
                item['query']=response.xpath('/html/head/title/text()')[0].extract().split(' - ')[0]
                
                article= Article(article_url,language='en')
                article.download()
                article.parse()
                
                date1=article.publish_date
                date2=str(response.xpath('//*[@id="tophf"]/input[@name="tbs"]/@value').extract()).split(',')[1].split(':')[1].replace('/','-')
                if date1 is None :
                    item['date']=date2
                    item['est_date']="True"
                else:
                    item['date']=str(date1)
                    item['est_date']="False"
                try :
                    content=article.text
                    item['content']=content
                    
                    # 주로 에러가 발생하면 시간초과 혹은 해당 사이트에서 크롤을 막았기 때문입니다.
                except :
                    item['content']="ERROR2"

                yield item

        #다음 페이지로 넘어갑니다.
        next_page=response.xpath('//*[@id="pnnext"]/@href')[0].extract()
        yield scrapy.Request(url=main_url+next_page,callback=self.parse,headers={'Content-Type':'text/html; charset=UTF-8','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'})
    
        