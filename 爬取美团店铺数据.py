import requests #发送请求
from bs4 import BeautifulSoup #解析页面
import pandas as pd #存入csv数据
import os #判断文件存在
from time import sleep #等待间隔
import random #随机
import re #用正则表达式提取url
import time #生成时间
import pprint #内置模块 -----导入格式化输出模块
import json
# 导入csv模块，内置模块
import csv
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Referer': 'https://chs.meituan.com/',
    'Host':'apimobile.meituan.com',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cookie':'......',
 def meituan_shop(result_file,Business_district,max_page,sort_choice):    
    """
    pass取美团店铺数据
    * result_file:保存文件名
    * Business_district:商圈
    * max_pageax: 爬取的页数
    * sort_choice:爬取排序选择
    """
    # 爬取的数据
    title_list = [] #店铺名
    cateId_list = [] # 店铺类别
    showType_list = [] #所属类型
    page_list = [] #页码
    avgscore_list = [] #评分
    areaname_list = [] #商圈
    avgprice_list = [] #人均消费
    backCateName_list = [] #店铺类型
    comments_list = [] #评论量
    id_list = [] #店铺id
    shop_url_list = [] #店铺url
    
    url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/70'
    for cateId in cateIds:
        if cateId == '1':
            cateId_name = '美食'
            shop_url_name = 'https://www.meituan.com/meishi/'
        elif cateId == '2':
            cateId_name = '休闲娱乐'
            shop_url_name = 'https://www.meituan.com/xiuxianyule/'
        else:
            cateId_name = '景点/周边游'
            shop_url_name = 'https://www.meituan.com//zhoubianyou/'
        for page in range(max_page):
            print(f'开始爬取_{cateId_name}_第{page+1}页')
            wait_seconds = random.uniform(1,2) #等待时长秒
            print('开始等待{}秒'.format(wait_seconds))
            sleep(wait_seconds) #随机等待
            data = {
                'uuid': 'e2609a7d40cc44dc85b4.1672580724.1.0.0',
                'userid': '1059531007',
                'limit': '32',
                'offset': page*32,
                # cateId代表是分类:美食1、休闲娱乐2、景点/周边游195
                'cateId': cateId,
                # 搜索地址
                'q':'五一广场',
                'token': 'AgGqJB1oR0GIL32aC3-ufCNJm0WJQDNgifpsWjYqudr-ZTt_izzDW2uTWg2Oy-gQ4IjyIdf13oxhagAAAACMFgAAQfzi-lckB8wIYuTS9VKde98rWPKtfh2isCERRjo4GOGE4Bo_YaG5XH1Cm9Pn17GQ',
                # 区域 五一广场4823
                'areald':'4823',
    #             'sort':sort_choice, 
            } #该数据为页面原码里的:Payload

            response = requests.get(url=url,params=data,headers=headers)
            print(response)
            searchRseult = response.json()['data']['searchResult']
    #         print(searchRseult)
            for index in searchRseult:
                title_list.append(index['title'])
                cateId_list.append(cateId_name)
                showType_list.append(index['showType'])
                page_list.append(page+1)
                avgscore_list.append(index['avgscore'])
                areaname_list.append(index['areaname'])
                avgprice_list.append(index['avgprice'])
                backCateName_list.append(index['backCateName'])
                comments_list.append(index['comments'])
                id_list.append(index['id'])
                shop_url_list.append(f'{shop_url_name}{index["id"]}/')
        df = pd.DataFrame(
            { 
                '店铺名':title_list,
                '店铺类别':cateId_list,
                '所属类型':showType_list,
                '页码':page_list,
                '评分':avgscore_list,
                '商圈':areaname_list,
                '人均消费':avgprice_list,
                '店铺类型':backCateName_list,
                '评论量':comments_list,
                'id':id_list,
                '店铺url':shop_url_list,
            }
        )
    # if os.path.exists(v_result_file):
    #     header = None
    # else:
    header = ['店铺名','店铺类别','所属类型','页码','评分','商圈','人均消费','店铺类型','评论量','id','店铺url'] #csv文件标题
    if os.path.exists(result_file):
        os.remove(result_file)
        print('结果文件({})存在，已删除'.format(result_file))
    df.to_csv(result_file,mode='a+',index=False,header=header,encoding='utf-8-sig')
    print('结果保存成功:{}'.format(result_file))   
if __name__=='__main__':
    Business_district = '五一广场'
    max_page = 10 #爬取的最大页码
    result_file = f'美团上{Business_district}的店铺_前{max_page}页.csv'
    if os.path.exists(result_file):
        os.remove(result_file)
        print('结果文件({})存在，已删除'.format(result_file))
#     sort_choice = 'rating' # 排序选择：人气最高solds，评价最高rating #将参数加入，程序有些问题
#     if sort_choice == 'rating':
#         sore_name = '评价最高'
#     else:
#         sore_name = '人气最高'
    #cateId = '1' # cateId代表是分类:美食1、休闲娱乐2、景点/周边游195
    cateIds = ['1','2','195']
#     for cateId in cateIds:
#         if cateId == '1':
#             cateId_name = '美食'
#             shop_url_name = 'https://www.meituan.com/meishi/'
#         elif cateId == '2':
#             cateId_name = '休闲娱乐'
#             shop_url_name = 'https://www.meituan.com/xiuxianyule/'
#         else:
#             cateId_name = '景点/周边游'
#             shop_url_name = 'https://www.meituan.com//zhoubianyou/'
    meituan_shop(result_file,Business_district,max_page,sort_choice)
