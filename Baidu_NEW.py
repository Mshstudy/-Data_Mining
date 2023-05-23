import requests #发送请求
from bs4 import BeautifulSoup #解析页面
import pandas as pd #存入csv数据
import os #判断文件存在
from time import sleep #等待间隔
import random #随机
import re #用正则表达式提取url
import time #生成时间
import datetime 
# 伪装浏览器请求头
headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'www.baidu.com',
    # 需要更换Cookie
    'Cookie':'BIDUPSID=C34B6AF4C13271404ADFB9411E76558C; PSTM=1658112630; BAIDUID=C34B6AF4C13271400346A4A423AE9988:SL=0:NR=10:FG=1; BDUSS=NVQ2xsSEM2eGdGOVZuRFlRMXlJR1d3cmZvS3E3RjUwUzF2dmNMZ0JoZ2l4VXhqSVFBQUFBJCQAAAAAAAAAAAEAAAAyQQiX0-7W5smtwdTIywAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACI4JWMiOCVjVl; BDUSS_BFESS=NVQ2xsSEM2eGdGOVZuRFlRMXlJR1d3cmZvS3E3RjUwUzF2dmNMZ0JoZ2l4VXhqSVFBQUFBJCQAAAAAAAAAAAEAAAAyQQiX0-7W5smtwdTIywAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACI4JWMiOCVjVl; MCITY=-342:; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=6; BAIDUID_BFESS=C34B6AF4C13271400346A4A423AE9988:SL=0:NR=10:FG=1; BA_HECTOR=a0a4818ga5818h24212g81hg1htgurm1l; ZFY=t6z0Y7xqnq6Bqxq:ArHKUnysnGHVwJ2cLXDk5YImT5RQ:C; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDRCVFR[C0p6oIjvx-c]=ddONZc2bo5mfAF9pywdpAqVuNqsus; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; ab_sr=1.0.1_ODM3MDhmYzlmN2UwNWUyYzgyMGQ1MDNiNWI3MzEzOGU0ZDQ1MDYwZDZkYWNkZDRjMGQ2YWRiMTVlYzA3ZTg3ZjFmOWZmOWFhMmU2ZWFjNjRhNzJmYjJlY2JiZjVkZjU4YTg3OTc0OTg4NDUyNDMyMzBmMDFkMzE1MGI4MTBlYWQ0MDk1ZDRmMjAzNGY4ZWU4MGIwNzY0NmNhMWM3YTk0Mw==; H_PS_PSSID=37782_36560_38091_37910_37989_37796_37927_38086_37959_38008_37881',
}

def date_transder(my_str ): #时间转换
    pattern = re.compile('(\d+)\D(\d+)\D(\d+)')
    dd = pattern.findall(my_str)
    date_strr0 = dd[0][0]+'-'+dd[0][1]+'-'+dd[0][2]
    date_strr =datetime.datetime.strptime(date_strr0 , "%Y-%m-%d")
    return date_strr
def baidu_search(v_keyword,v_result_file,v_max_page):
    """
    爬取百度搜索结果
    :param v_max_page:爬取前几页
    :param v_keyword: 搜索关键字
    :param v_result_file:保存文件名
    """
    #获取每页搜索结果
    for page in range(v_max_page):
        print('开始爬取第{}页'.format(page+1))
        wait_seconds = random.uniform(1,2) #等待时长秒
        print('开始等待{}秒'.format(wait_seconds))
        sleep(wait_seconds) #随机等待
        #https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=&pn=30
        #url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd='+ v_keyword+'&medium=0&pn='+str(page*10)
        url = 'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=4&bsst=1&rsv_dl=news_b_pn&cl=2&wd='+v_keyword+'&medium=0&pn='+str(page*10)
        r = requests.get(url,headers=headers)
        html = r.text
        print('响应码是:{}'.format(r.status_code)) #响应码为200时，正常返回
        soup = BeautifulSoup(html,'html.parser') #解析页面
        result_list0 =  soup.find_all(class_='result-op c-container new-pmd')
        result_list1 = soup.find_all(class_='result-op c-container xpath-log new-pmd')
        result_list = result_list0+result_list1
        print('正在爬取:{},共查询{}个结果'.format(url,len(result_list)))
        kw_list = [] #关键字
        page_list = [] #页码
        title_list = [] #标题
        release_time_list = [] #发布时间
        crawling_time_list = [] #爬取时间
        href_list = [] #百度的链接
        real_url_list = []#真实的链接
        desc_list = [] #简介
        site_list = [] #网站名称
        for result in result_list:
            title = result.find('a').text #找出第一个a
            #print('title is :',title)
            href = result.find('a')['href']
            try:
                release_time1 = result.find(class_='c-color-gray2').text
                #print(len(release_time1))
                if len(release_time1) > 8:
                    release_time2 = date_transder(release_time1)
                    #print(release_time2)
#                     release_time3 = datetime.datetime.strptime(release_time2, "%Y-%m-%d")
#                     print(release_time3)
                    release_time = release_time2
                    #print(release_time2 < start_time)
                    if release_time2 < start_time:
                        print(f'发布时间已小于{start_time},停止爬取')
                        break
                else:
                    release_time = release_time1
            except:
                release_time=""
#             print(release_time)
            crawling_time =  time.strftime("%Y-%m-%d",time.localtime())
            try:
                desc=result.find(class_='c-font-normal c-color-text').text
            except:
                desc=""
            try:
                site = result.find(class_='c-color-gray').text
            except:
                site = ""
            kw_list.append(v_keyword)
            page_list.append(page+1)
            title_list.append(title)
            release_time_list.append(release_time)
            crawling_time_list.append(crawling_time)
            href_list.append(href)
            desc_list.append(desc)
            site_list.append(site)
        df = pd.DataFrame(
            {
                '关键字':kw_list,
                '页码':page_list,
                '标题':title_list,
                '发布时间':release_time_list,
                '爬取时间':crawling_time_list,
                '百度链接':href_list,
                '简介':desc_list,
                '网站名称':site_list,
            }
        )
        if os.path.exists(v_result_file):
            header = None
        else:
            header = ['关键字','页码','标题','发布时间','爬取时间','百度链接','简介','网站名称'] #csv文件标题
        df.to_csv(v_result_file,mode='a+',index=False,header=header,encoding='utf-8-sig')
    print('结果保存成功:{}'.format(v_result_file))   
    
if __name__=='__main__':
    search_keyword_list = ['长沙夜经济','长沙夜消费','夜长沙','长沙夜市','长沙夜生活',
                           '长沙夜游','长沙夜间','长沙夜宵','长沙夜食','长沙夜娱'] #搜索的关键词
    start_time = datetime.datetime.strptime("2022-01-01", "%Y-%m-%d") #开始爬取百度时间
    result_file = '爬取百度-夜长沙.csv'
    if os.path.exists(result_file):
        os.remove(result_file)
        print('结果文件({})存在，已删除'.format(result_file))
    for search_keyword in search_keyword_list:
        max_page = 10
        baidu_search(v_keyword=search_keyword,v_result_file=result_file,v_max_page=max_page)
#     result_file = '爬取百度新闻_{}_前{}页.csv'.format(search_keyword,max_page) #保存结果的文件名
    # 如果结果文件存在，先删除
    
    
    
