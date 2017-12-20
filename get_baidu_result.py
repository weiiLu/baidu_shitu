#-*- coding: utf8 -*-
import urllib2
import time
import random
import chardet
from bs4 import BeautifulSoup

def getHtml(url,retries=3):
    """
    获取指定地址的html内容
    :url:网址
    """

    try:
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11' }
        req = urllib2.Request(url)
        page = urllib2.urlopen(req,timeout = 60)
        html = page.read()
        return html
    except  Exception , what:
        if retries>0:
            print "retry the url!"
            return getHtml(url,retries-1)
    # except urllib2.HTTPError as e:
    #     print "获取html失败！失败原因如下：\n"
    #     print e.code, e.reason
    # req = urllib2.Request(url)
    # page = urllib2.urlopen(req,timeout = 1000)
    # html = page.read()
    # return html

def get_baidu_predict(url,num = 5):
    """
    从百度识图中获取预测类别
    url:待解析的网页地址,一般为拼凑而成
    num:返回的预测数目，最多为５
    """

    try:
        html = getHtml(url)
        soup = BeautifulSoup( html , "html.parser" ) #使用bs库解析html
        predict_value1 = [] #存放预测结果初始筛选值
        predict_value2 = [] #存放最终结果

        #class = "guess-info-text"只能识别一类
        guess_tag = len(soup.find_all("div",class_ = "guess-info-text"))

        #class = "guess-info-not-found"无法识别，只能猜测;tag = 1,无法识别；tag = 0　可以被识别
        tag = len(soup.find_all("div",class_="guess-info-not-found"))

        #
        shitu_tag = len(soup.find_all("ul",class_="shituplant-tag"))
        #百度识图成功则结果字串存放于<ul>的<li>标签下,失败则只有<ol>标签
        #print tag,soup.ol
        if (soup.ol is None and tag == 0) :
            #识图成功
            #guess_tag = 1 百度猜测
            if guess_tag != 0:
                predict_value2 = soup.find_all("a",class_ = "guess-info-word-link guess-info-word-highlight")[0].get_text()
                return 2,predict_value2
            elif shitu_tag != 0:
                #百度识图，给出top-5的标签
                for child in soup.ul.children:
                    predict_value1.append(unicode(child.string))
                #剔除冗余信息
                for value in range(len(predict_value1)/2):
                    predict_value2.append(predict_value1[value * 2 + 1])
                if num > 5:
                    print("最多只能得到排名前五的预测结果！")
                    return 1,predict_value2
                else:
                    return 0,predict_value2[:num]
            else:
                return 3,predict_value2
        else:
            #识图失败
            return 3,predict_value2
    except Exception as e:
        #print('爬虫错误，错误原因：',e)
        print "爬取网页失败！"



def get_ground_truth(txtfile):
    """
    将tag-label以字典的形式存储起来
    """

    dict_value = dict()
    try:
        with open(txtfile,'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                items = line.split(' ')
                dict_value[items[1]] = items[2]
    except IOError:
        print txtfile + ' not found,please check it again or you don\'t have permission to access this file.'

    return dict_value

dict_value = get_ground_truth('label_cid_word_530.txt')
with open('urlList_label.txt','r') as f, open('baidu_pre.txt','w') as f2:
    test_num = 0  #统计测试样本数目
    top_5_error_num = 0. #统计top-5识别错误数目
    top_1_error_num = 0. #统计top-1识别错误数目
    result = ''

    for line in f.readlines():
        sign = False  #top-5识别正确与否的标志
        pre_info = ''
        line = line.strip('\n')
        items = line.split(' ')

        ground_truth = dict_value[items[1]].decode('utf-8')

        if items[0] is None:
            print 'items is None,when loading the url!'
            break
        tag,pre = get_baidu_predict(items[0])
        if tag == 0:
            #识图成功
            pp = ''
            for val in pre:
                # print chardet.detect(pre[0])
                # print chardet.detect(dict_value[items[1]]),dict_value[items[1]].decode('utf-8')
                if val == ground_truth:
                    sign = True
                pp = val + ' '
            pre_info = '第' + str(test_num)+'张->预测值:'+ pre[0].encode('utf-8') + '  ground_truth:' + ground_truth.encode('utf-8') + '\n'
            if pre[0] != ground_truth:
                top_1_error_num += 1
        elif tag == 1:
            #识图成功,但预测结果超过索引
            break
        elif tag == 2:
            #识图成功，百度猜测
            pre_info = '第' + str(test_num)+'张->预测值:'+ pre.encode('utf-8') + '  ground_truth:' + ground_truth.encode('utf-8') + '\n'
            if pre == dict_value[items[1]].decode('utf-8'):
                sign = True
            else:
                top_1_error_num += 1
        else:
            #tag = 3 识图失败
            sign = False
            top_1_error_num += 1
            pre_info  = '第' + str(test_num)+'张->识图失败:'+ '  ground_truth:' +ground_truth.encode('utf-8') + '\n'

        if sign is False:
            top_5_error_num += 1

        test_num += 1
        print ("正在识别第{}张图．．．".format(test_num))
        if len(pre) != 0 :
            if tag == 0:
                print ("预测最有可能是{}，ground_truth：{},识图结果{}".format(pre[0].encode('utf-8'),dict_value[items[1]],sign))
            elif tag == 2:
                print ("预测最有可能是{}，ground_truth：{},识图结果{}".format(pre.encode('utf-8'),dict_value[items[1]],sign))
            else:
                print 'index out of range'
        else:
            print ("百度识图失败．．．.............")
        result += pre_info
    f2.writelines(result)
    print top_1_error_num,top_5_error_num,test_num
    print("top-1 error_rate:{:.4f}".format(top_1_error_num/test_num))
    print("top-5 error_rate:{:.4f}".format(top_5_error_num/test_num))
