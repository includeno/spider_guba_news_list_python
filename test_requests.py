import requests
import time
import os
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from spider import parse_html_js_data
from utils import write_json_data,write_page_csv_data,write_merged_csv_data,write_page_info_csv_data
from logging import getLogger

logger=getLogger("test_requests")

# html = ""
# url = "http://guba.eastmoney.com/list,usaapl_1.html"
# response = requests.get(url)
# print("text:",response.text)
# print("encoding:",response.encoding)
# print("status_code:",response.status_code)

def save_response(stock):
    url = f"http://guba.eastmoney.com/list,{stock},99,j_1.html"
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join("responses", f"response_{stock}.html")
        with open(filename, 'w') as f:
            f.write(response.text)
        print(f"Saved {url} to {filename}",flush=True)
    else:
        print(f"Failed to fetch {url}",flush=True)
    time.sleep(4)
    logger.info(f"Saved {url} to {filename}")

def main(stocks):
    #stocks=["usaapl","usamzn","usnflx","usgoog","usfb"]

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures=[]
        for stock in stocks:
            futures.append(executor.submit(save_response, stock))
        # 遍历 Future 对象，获取执行结果
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(f"result:{result}",flush=True)
            except Exception as e:
                print(f"An error occurred: {e}")
    
    print("Done!")
    page_info_csv_file_path=""
    # 解析每一个html文件
    for stock in stocks:
        filename = os.path.join("responses", f"response_{stock}.html")
        
        with open(filename, 'r') as f:
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
            print("stock:",stock,"count:",count,"page_count:",page_count,"stock_code:",stock_code)
            page_info_csv_file_path=write_page_info_csv_data(stock,page_count,count)
    return page_info_csv_file_path

if __name__ == '__main__':
    stocks=["usaapl","usamzn","usnflx","usgoog","usfb"]
    main(stocks)






