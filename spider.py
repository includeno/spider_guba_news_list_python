from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium_driver import get_driver_by_system,get_firefox_driver_options
import json
from utils import write_json_data,write_page_csv_data,write_merged_csv_data,write_page_info_csv_data
import requests

# 测试通过
def get_list_url_by_page(stock,page):
    if(page==1):
        return f"http://guba.eastmoney.com/list,{stock}.html"
    else:
        return f"http://guba.eastmoney.com/list,{stock}_"+str(page)+".html"

# 完成
def write_html_request(url,driver=None,html_file=None,implicit_wait=20,page_load_timeout=30,sleep_time=4):
    html = ""
    response = requests.get(url)
    if(response.status_code!=200):
        print("response error",response.status_code,flush=True)
        raise Exception("response error")
    html = response.text
    print(f"get url succeed:{url}",flush=True)
    
    # 页面源代码写入文件
    import uuid
    if(html_file==None):
        html_file=uuid.uuid4().hex+".txt"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
        print(f"write html succeed:{html_file}",flush=True)
    time.sleep(sleep_time)
    return html_file

# 测试通过
def write_html(url,driver=None,html_file=None,implicit_wait=20,page_load_timeout=30,sleep_time=4):
    if(driver==None):
        driver = get_driver_by_system()
    if(driver==None):
        print("driver does not exist",flush=True)
        raise Exception("system driver error")
    # 设置最大等待时间为10秒
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    driver.get(url)
    html = ""
    try:
        driver.get(url)
        html = driver.page_source
        print(f"get url succeed:{url}",flush=True)
    except Exception as e:
        print("driver error",e,flush=True)
        html = driver.page_source
    finally:
        html = driver.page_source
        driver.quit()
    # 页面源代码写入文件
    import uuid
    if(html_file==None):
        html_file=uuid.uuid4().hex+".txt"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
        print(f"write html succeed:{html_file}",flush=True)
    time.sleep(sleep_time)
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

def crawl_stock_list_by_page(stock,page,stock_code):
    url=get_list_url_by_page(stock,page)
    result=[]
    filename=f"json_temp_{stock}.txt"
    html_file=write_html(url,driver=None,html_file=filename)
    html=""
    # 读取文件
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    if(html==""):
        print("html is empty",flush=True)
    # 删除文件
    import os
    os.remove(html_file)
    print(f"html_file:{html_file} removed",flush=True)
    js=parse_html_js_data(html)
    write_json_data(js,f"{stock}_{page}.json")
    for item in js["re"]:
        # json 格式转化为dict
        data={
            "title":item["post_title"],
            "id":item["post_id"],
            "username":item["user_nickname"],
            "user_id":item["user_id"],
            "comment_count":item["post_comment_count"],
            "time":item["post_publish_time"],
            "stock_code":stock_code,
            "stockbar_name":item["stockbar_name"]
            }
        result.append(data)
    page_csv_file_path=write_page_csv_data(result,stock=stock,page=page)
    return result

def get_table_info(stock):
    url=get_list_url_by_page(stock,1)
    html_file=""
    try:
        html_file=write_html(url,driver=None,html_file=f"html_{stock}.txt",implicit_wait=10,page_load_timeout=35,sleep_time=2)
    except Exception as e:
        print("get_table_info error",e,flush=True)
    html=""
    # 读取文件
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    js=parse_html_js_data(html)
    print("bar_name:",js["bar_name"])
    count=js["count"]
    page_count=(count + 79) // 80
    print("page_count:",page_count)
    print("count:",count)
    print("StockCode:",js["bar_info"]["StockCode"])
    print("bar_name:",js["bar_name"])
    stock_code=js["bar_info"]["StockCode"]
    print("stock_code:",stock_code)

    # 删除文件
    import os
    os.remove(html_file)
    print(f"html_file:{html_file} removed",flush=True)
    return count,page_count,stock_code

def get_table(stock,max_page=1,page_count=None,stock_code=None):
    script='window.scrollTo(0, document.body.scrollHeight);'
    if(page_count is None or stock_code is None):
        count,page_count,stock_code=get_table_info(stock)
    
    merged_csv_file_path=""
    result_list=[]
    error_pages=[]
    for page in range(1,page_count+1):
        if(max_page is not None and page>max_page):
            break
        result=[]
        try:
            result=crawl_stock_list_by_page(stock,page,stock_code)
        except Exception as e:
            print(f"crawl_stock_list_by_page error ,adding page:{page}",e,flush=True)
            error_pages.append(page)
            time.sleep(10)
            continue
        for data in result:
            result_list.append(data)
        merged_csv_file_path=write_merged_csv_data(result_list,stock=stock)
    for page in error_pages:
        if(max_page is not None and page>max_page):
            break
        result=[]
        try:
            result=crawl_stock_list_by_page(stock,page,stock_code)
        except Exception as e:
            print("crawl_stock_list_by_page error_pages!",e,flush=True)
        for data in result:
            result_list.append(data)
        merged_csv_file_path=write_merged_csv_data(result_list,stock=stock)
    return merged_csv_file_path

def get_page_info(stock):
    print("get_page_info:",stock,flush=True)
    count,page_count,stock_code=get_table_info(stock)
    print("stock:",stock,"count:",count,"page_count:",page_count,"stock_code:",stock_code)
    write_page_info_csv_data(stock,page_count,count)
    return count,page_count,stock_code

if __name__ == "__main__":
    print()
    #merged_csv_file_path=get_table("usamzn",max_page=7)
    #merged_csv_file_path=get_table("usdjia",max_page=2)
    #print("merged_csv_file_path:",merged_csv_file_path)