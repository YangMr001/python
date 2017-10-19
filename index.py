import json
import os
import urllib
import requests
from bs4 import BeautifulSoup
import time
import csv
import codecs
from selenium import webdriver

csv_file = codecs.open('rent.csv', 'ab', 'utf-8', 'ignore')
csv_writer = csv.writer(csv_file)

headers = {
'Accept:application/json, text/javascript, */*':'q=0.01',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Content-Length':'31',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Host':'www.lagou.com',
'Origin':'https://www.lagou.com',
'Referer':'https://www.lagou.com/jobs/3682270.html',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'X-Anit-Forge-Code':'94367310',
'X-Anit-Forge-Token':'087ef3df-ae1a-41e2-8b58-86e4bd6652c3',
'X-Requested-With':'XMLHttpRequest'
}
cookies = {'Cookie':'user_trace_token=20171010215205-33775b9d-adc2-11e7-9470-5254005c3644; '
                   'LGUID=20171010215205-3377642c-adc2-11e7-9470-5254005c3644;'
                   ' ab_test_random_num=0; JSESSIONID=ABAAABAAAGGABCB4226482E50622268B92013BA29C39B41; '
                   '_putrc=54D6D44AC87A2A52; login=true; unick=%E6%9D%A8%E9%B9%8F%E5%8D%87; showExpriedIndex=1; '
                   'showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=2; TG-TRACK-CODE=index_navigation;'
                   ' PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F;'
                   ' PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FPython%2F%3FlabelWords%3Dlabel; '
                   '_gid=GA1.2.227902757.1508126408; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508126572,1508129091,1508144071,1508144075;'
                   ' Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508144682; _ga=GA1.2.1552764521.1507643525;'
                   ' LGSID=20171016165435-a2764461-b24f-11e7-9582-5254005c3644; LGRID=20171016170439-0a9caee9-b251-11e7-9582-5254005c3644; '
                   'SEARCH_ID=5aaf16723a5740f89858bc9e8a24eda2;'
                   ' index_location_city=%E5%8C%97%E4%BA%AC'}

def post(url,para,headers=None,cookies=None,proxy=None,timeOut=5,timeOutRetry=5):
    if not url or not para:
        print("PostError url or para not exit")
        print("11111111111111")
        return None
    try:
        if not headers:
            headers=headers
        response = requests.post(url,data=para,headers=headers,cookies=cookies)
        if response.status_code == 200 or response.status_code == 302:
            htmlCode =  response.text
        else:
            print("2222222222222")
            htmlCode = None
    except Exception as e:
        if timeOutRetry > 0:
            htmlCode = post(url=url,para=para,timeOutRetry=(timeOutRetry-1))
            print('3333333333333333333333333333')
            htmlCode = None
    return htmlCode

url = 'https://www.lagou.com/jobs/positionAjax.json?'
para = {'first':'true','pn':'1','kd':'python','city':'北京','needAddtionalResult':'false','isSchoolJob':0}

def getinfo(url,para):

    htmlCode = post(url,para=para,headers=headers,cookies=cookies)   #获取到网页源码,一大堆的json数据
    info = {}
    print(htmlCode)
    # soup = BeautifulSoup(htmlCode,'html.parser')
    if htmlCode == None:
        return False
    companies = htmlCode.get('content').get('positionResult').get('result')
    for i in companies:
        info['公司名字'] = companies[i]['companyFullName']              #公司名字
        info['招聘职位'] = companies[i]['positionName']              #招聘职位
        info['发布时间'] = companies[i]['formatCreateTime']              #发布时间
        info['薪资待遇'] = companies[i]['salary']              #薪资待遇
        info['经验要求'] = companies[i]['workYear']              #经验要求
        info['公司大小'] = companies[i]['companySize']              #公司大小
        info['公司福利'] = companies[i]['positionAdvantage']              #公司福利
        info['公司地址'] = companies[i]['company']              #公司地址
        csv_writer.writerow(companies[i]['companyFullName'],companies[i]['positionName'],companies[i]['formatCreateTime'],companies[i]['salary'],
                            companies[i]['workYear'],companies[i]['companySize'],companies[i]['positionAdvantage'],companies[i]['company'])


if __name__ == '__main__':
    getinfo(url,para)