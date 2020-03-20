# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 15:21:11 2019

@author: franc_000
"""

##########################
### 키워드 및 날짜 지정 ###
##########################
import pandas as pd

class SearchInformation :
    #query = 'intel'
    data=pd.read_csv("query_list.csv",encoding='ms949')
    query_list=data['query'].values.tolist()
    str_from_date="2019.07.01"
    
    # Desktop/데이터몬스터즈/Project2/Scrapy_GoogleNews