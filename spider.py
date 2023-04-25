from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium_driver import get_driver_by_system,get_firefox_driver_options
import json
from utils import write_json_data,write_page_csv_data,write_merged_csv_data

# 测试通过
def get_list_url_by_page(stock,page):
    if(page==1):
        return f"http://guba.eastmoney.com/list,{stock}.html"
    else:
        return f"http://guba.eastmoney.com/list,{stock}_"+str(page)+".html"

# 测试通过
def write_html(url,driver=None,html_file="html.txt"):
    if(driver==None):
        driver = get_driver_by_system()
    if(driver==None):
        print("driver does not exist",flush=True)
        raise Exception("system driver error")
    driver.get(url)
    time.sleep(1)
    result=[]
    # 设置最大等待时间为10秒
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(15)
    html = ""
    try:
        driver.get(url)
        html = driver.page_source
    except Exception as e:
        print("driver error",e,flush=True)
        html = driver.page_source
    finally:
        driver.quit()
    # 页面源代码写入文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    return html_file

# 测试通过
def parse_html_js_data(html):
    bs = BeautifulSoup(html, 'html.parser')
    # 找到包含data变量的script标签
    script_tag = bs.select_one('script:contains("var article_list")')

    # 提取data变量的值
    data_str = script_tag.string.split('=', 1)[1].strip()
    list_of_data=data_str.split(";")

    # 第一部分是列表+评论+基本信息 
    json_data = json.loads(list_of_data[0])
    return json_data

def get_table(stock,max_page=1):
    script='window.scrollTo(0, document.body.scrollHeight);'
    url=get_list_url_by_page(stock,1)
    temp=write_html(url,driver=None,html_file="html.txt")
    html=""
    # 读取文件
    with open(temp, 'r', encoding='utf-8') as f:
        html = f.read()
    js=parse_html_js_data(html)
    print("count:",js["count"])
    print("StockCode:",js["bar_info"]["StockCode"])
    print("bar_name:",js["bar_name"])
    count=js["count"]
    page_count=int(count/80+0.5)
    stock_code=js["bar_info"]["StockCode"]
    
    merged_csv_file_path=""
    for page in range(1,page_count):
        if(max_page!=None and page>max_page):
            break
        url=get_list_url_by_page(stock,page)
        result=[]
        html_file=write_html(url,driver=None,html_file="json-temp.txt")
        html=""
        # 读取文件
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()
        js=parse_html_js_data(html)
        write_json_data(js,f"{stock}_{page}.json")
        for item in js["re"]:
            # json 格式转化为dict
            result.append({
                "title":item["post_title"],
                "id":item["post_id"],
                "username":item["user_nickname"],
                "user_id":item["user_id"],
                "comment_count":item["post_comment_count"],
                "time":item["post_publish_time"],
                "stock_code":stock_code,
                "stockbar_name":item["stockbar_name"]
                })
        page_csv_file_path=write_page_csv_data(result,stock=stock,page=page)
        merged_csv_file_path=write_merged_csv_data(result,stock=stock)
    return merged_csv_file_path

if __name__ == "__main__":
    get_table("usmsft",max_page=2)