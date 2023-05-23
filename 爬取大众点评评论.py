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
import csv # 导入csv模块，内置模块
import datetime
from parsel import Selector
from lxml import etree
#请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'www.dianping.com',
    'Referer': 'https://www.dianping.com/shop/k7a1VkZePZmh0ZxC/review_all?queryType=sortType&&queryVal=latest',
    # 需要更换
    'Cookie':'_lxsdk_cuid=186029fe91813-040779a19a4ea7-26021151-144000-186029fe919c8; _lxsdk=186029fe91813-040779a19a4ea7-26021151-144000-186029fe919c8; _hc.v=664a445f-e4c9-0532-1093-babfed4ce403.1675081280; cy=344; cye=changsha; s_ViewType=10; WEBDFPID=7v9192y335385y5213860u038u02xu1481397z4787w9795871850uy7-1990441622133-1675081620857EAOKKCOfd79fef3d01d5e9aadc18ccd4d0c95073392; ctu=5f01cf51de0a24777fc2b771a1a817802ddb9eba737605b98d87458ffce51ccd; ua=dpuser_4225374526; pvhistory=5Zu+54mH6K+m5oOFPjo8L3Bob3Rvcy85MDkyMDUzMzY+OjwxNjc3NjU4NTM3NDcyXV9b; m_flash2=1; qruuid=37cf133b-3736-406f-b5c7-8b117bad0c74; dplet=0e495e4cea35095b38d2a6f2a7f3f07c; dper=930ce1d6ae687c27eec63a8a39865728f039da5ddf414318d4a2569ead4026a89ba7bbea1118ce875a16054d0a5f4179c93773b523869b7061aa119f733ee8a7; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1675515903,1675754844,1677660273; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1677982919; _lxsdk_s=186af9364c2-67e-162-c28||81',
}
def SvgDeclassify(url,r):
    '''
    * url : 需要解密的链接
    * r: 爬取获得的页面
    * 获取css文件
    * 请求svg内容
    '''
    print('爬取的url：',url)
    with open('dazhong.html','w',encoding='utf-8') as f:
        f.write(r.text)
    css_url = re.findall('<link rel="stylesheet" type="text/css" href="(//s3plus.meituan.*?)">',r.text)
    css_url = 'https:'+ css_url[0]
    # print(css_url)
    css_response = requests.get(css_url)
    with open('dazhong.css',mode='w',encoding='utf-8') as f:
        f.write(css_response.text)
    svg_url = re.findall(r'svgmtsi\[class\^="ek"\]\{.*?background-image: url\((.*?)\);',css_response.text)
    svg_url = 'http:'+ svg_url[0]
    svg_response = requests.get(svg_url)
    with open('dazhong.svg',mode='w',encoding='utf-8') as f:
        f.write(svg_response.text)
    # print(svg_url)
    # 解密svg加密内容
    with open('dazhong.svg',mode='r',encoding='utf-8') as f:
        svg_html = f.read()
    sel = Selector(svg_html)

    # 加载映射规则表
    # texts = sel.css('textPath') #当为<textPath>时
    texts = sel.css('text')
    svg_x = 0
    lines = []
    for text in texts:
        svg_x += 1
    #     svg_y = text.css("textpath::attr(textlength)").get()
    #     svg_text = text.css("textpath::text").get()
        svg_y = text.css("text::attr(y)").get()
        svg_text = text.css("text::text").get()
        lines.append([svg_x,int(svg_y),svg_text])

    """  获取所有的类名，与位置 """
    with open('dazhong.css',mode='r',encoding='utf-8') as f:
        css_text = f.read()
    class_map = re.findall('\.(ek\w+){background:-(\d+)\.0px -(\d+)\.0px;\}',css_text)
    class_map = [(cls_name,int(x),int(y)) for cls_name, x, y in class_map]
    # print(class_map)
    # print(lines)
    svg_map = []
    d_map ={}
    # 获取类名与汉字的对应关系
    for one_char in class_map:
        try:
            cls_name,x,y = one_char
    #         print(one_char)
            for line in lines:
    #             print(line)
                if line[1] < y:
                    pass
                else:
                    #字符所在的位置
                    index = int(x/14)
                    char = line[2][index]
    #                 print('当前待匹配的字符串：',one_char)
    #                 print('当前待匹配的行：',line)
    #                 print(cls_name,char)
                    d_map[cls_name] = char
                    svg_map.append([cls_name,char])
                    # 匹配到一个内容之后，应该结束当前的匹配，去匹配下一个字符
                    break
        except Exception as e:
            print(e)

    # print(d_map)
    with open('dazhong.html',mode='r',encoding='utf-8') as f:
        html_1 = f.read()
    # print(type(html0))
    svg_list = re.findall('<svgmtsi class="(.*?)"></svgmtsi>', html_1)
    for svg in svg_list:
        html_1 = html_1.replace(f'"{svg}"',d_map[svg])
    html = html_1.replace('<svgmtsi class=', '').replace('></svgmtsi>', '') 
    ret = html.replace('<div class="richtitle">消费后评价</div>', '')
    etre = etree.HTML(ret)
    li_list = etre.xpath('//div[@class="reviews-items"]/ul/li')
    review_list = []
    for i in li_list:
        review_A = i.xpath('div[@class="main-review"]/div[@class="review-words Hide"]/text()')
        review_B = str(review_A).replace('"',"").lstrip("['").rstrip("']").replace('\\n',"").replace(" ","").replace("'","")
        review_list.append(review_B)
    return review_list
  def dazhong_review(max_page,shop_keywords,start_time,end_time ):
    '''
    # 爬取大众点评评论数据
    * max_page:爬取最大页数
    '''
    for page in range(170,max_page):
        print('开始爬取第{}页'.format(page+1))
        wait_seconds = random.uniform(1,2) #等待时长秒
        print('开始等待{}秒'.format(wait_seconds))
        sleep(wait_seconds) #随机等待
        url = f'https://www.dianping.com/shop/{shop_keywords}/review_all/p{page+1}?queryType=sortType&queryVal=latest'
        r = requests.get(url,headers=headers)
        html = r.text
#         print(html)
        print('响应码是:{}'.format(r.status_code)) #响应码为200时，正常返回 
        try:
            comment_review = SvgDeclassify(url=url,r=r) #每页的评论内容
        except:
            comment_review = ""
        soup = BeautifulSoup(html,'html.parser') #解析页面
        try:
            shopname = soup.find(class_= 'shop-info clearfix').text.strip()
        except:
            shopname = ""
        reviews_result_list = soup.find_all(class_ = 'main-review')
        n = len(reviews_result_list) #该页的评论数量 
        print('正在爬取:{},共查询{}个结果'.format(url,n))
        shopname_list = [] #店铺名
        page_list = [] #页码
        username_list = [] #用户名
        taste_score_list = [] #口味评分
        environmental_score_list = [] #环境评分
        service_score_list = [] #服务评分
        costperformance_score_list = [] #性价比评分
        avgprice_list = [] #人均消费
        reviews_list = [] #评论内容
        comment_time_list = [] #评论时间
        YMD_list = [] #评论时间的--年月日
        HM_list = [] #评论时间的--时分
        L_time1 = datetime.datetime.strptime("6:00", "%H:%M")
        L_time2 =  datetime.datetime.strptime("18:00", "%H:%M")
        for i in range(n):
            result = reviews_result_list[i]
            username = result.find('a').text.strip() #str.strip(chart) 删掉开头结尾的字符
            try:
                taste_score = result.find_all(class_='item')[0].text.strip().lstrip("口味：")
                environmental_score = result.find_all(class_='item')[1].text.strip().lstrip("环境：")
                service_score = result.find_all(class_='item')[2].text.strip().lstrip("服务：")
            except:
                taste_score = ""
                environmental_score = ""
                service_score = ""
            try:
                costperformance_score = result.find_all(class_='item')[3].text.strip().lstrip("性价比：")
            except:
                costperformance_score = ""
            try:
                reviews = comment_review[i]
            except:
                reviews = ""
            #avgprice = result.find_all(class_='item')[4].text
#             try:
#                 reviews = result.find(class_ = 'review-words').text.replace(" ", "").replace("\n","").rstrip("收起评价")
#             except:
#                 reviews = ""
            try:
                comment_time = result.find(class_ = 'time').text.strip()
        #         print(type(list(comment_time)))
                if(len(comment_time)>16):
                    comment_time = re.findall("于(.*?)$",comment_time) #选择更新后的评论时间
                    comment_time = str(comment_time).lstrip("['").rstrip("']")

            except:
                comment_time = ""
            '''
            # 对评论时间进行筛选：
            * 选择参与夜经济的评论时间：18:00-第二天6:00
            * 选择开始时间以后的评论
            '''    
            Ymd0 = re.split(" ",comment_time)[0] #分割后的年月日
            HS0 = re.split(" ",comment_time)[1]  #分割后的小时分钟
            Ymd = datetime.datetime.strptime(Ymd0, "%Y-%m-%d")
            HS = datetime.datetime.strptime(HS0,"%H:%M") 
            if Ymd < start_time:
                break
            if HS > L_time1 and HS < L_time2:
                continue
            shopname_list.append(shopname)
            page_list.append(page+1)
            username_list.append(username)
            taste_score_list.append(taste_score)
            environmental_score_list.append(environmental_score)
            service_score_list.append(service_score)
            costperformance_score_list.append(costperformance_score)
            comment_time_list.append(comment_time)
            YMD_list.append(Ymd0)
            HM_list.append(HS0)
            reviews_list.append(reviews)
        df = pd.DataFrame(
            {
                '店铺名':shopname_list,
                '页码':page_list,
                '用户名':username_list,
                '口味评分':taste_score_list,
                '环境评分':environmental_score_list,
                '服务评分':service_score_list,
                '性价比评分':costperformance_score_list,
                '评论时间':comment_time_list,
                '时间YMD':YMD_list,
                '时间HM':HM_list,
                '评论内容': reviews_list,
            }
        )   
        if os.path.exists(result_file):
            header = None
        else:
            header = ['店铺名','页码','用户名','口味评分','环境评分','服务评分','性价比评分','评论时间',
                       '时间YMD','时间HM','评论内容'] #csv文件标题
        df.to_csv(result_file,mode='a+',index=False,header=header,encoding='utf-8-sig')
#         if Ymd < start_time:
#             break
    print('结果保存成功:{}'.format(result_file)) 

if __name__=='__main__':
    '''
    #店铺id：
    * H6rn3U2sZsH8aTM7(茶颜悦色(国金一店)) --56页 √
    * k5GYBU1J8FvjWPsC(费大厨辣椒炒肉(7mall店))--106页√
    * H2UX6qCjp5bJBICK(虾小龙老长沙龙虾馆(五一广场店)) --215页
    * GarIEcDuE58PvWgR(城市英雄Party House(五一广场店))--29页√
    * EhUKmiRtvBQ3tqhK(长藤鬼校(解放西路店)) -- 21页 √
    * H4hz84R9GW4jPjst(名侦探密室·剧本(五一广场店)) --5页 √
    * H2cyeH6srn0M9if0(橘子洲景区) --148页  √
    '''
    shop_keywords = 'H2UX6qCjp5bJBICK'
    max_page = 190 #最大页码数
    start_time = datetime.datetime.strptime("2022-01-01", "%Y-%m-%d") #开始爬取评论时间
    end_time = datetime.datetime.strptime("2023-01-01", "%Y-%m-%d") #结束爬取评论时间
    result_file = '爬取(虾小龙老长沙龙虾馆(五一广场店)1)大众点评评论.csv'
#     if os.path.exists(result_file):
#         os.remove(result_file)
#         print('结果文件({})存在，已删除'.format(result_file))
    dazhong_review(max_page=max_page,shop_keywords = shop_keywords,start_time = start_time,end_time = end_time )
    
