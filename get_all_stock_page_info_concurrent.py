# 从stocks.csv提取所有的股票代码
import pandas as pd
from spider import get_page_info
from utils import write_page_info_csv_data,read_page_info_csv_data
# # 定义添加前缀和小写化的函数
# def add_prefix_and_lowercase(text, prefix):
#     return prefix + text.lower()
# prefix = 'us'
# stocks_df=pd.read_csv('stocks.csv')
# # 为某列添加前缀并将原文本小写化
# stocks_df['name_en'] = stocks_df['name_en'].apply(lambda x: add_prefix_and_lowercase(x, prefix))
# li=stocks_df['name_en'].values.tolist()
# # 去除重复的股票代码和包含_,.的股票代码
# li=list(set(li))
# li=[i for i in li if '_' not in i]
# li=[i for i in li if '.' not in i]
# li=[i for i in li if ' ' not in i]
# li=[i for i in li if '-' not in i]
# print(len(li))
# print(li)

# df=read_page_info_csv_data()
# stocks=df["stock"].values.tolist()
# print("stocks:",stocks)

#max_count=100
max_count=None

# for stock in li:
#     #去除csv中已经存在的股票代码
#     if(stock in stocks):
#         continue
#     stock_count=stock_count+1
#     if(stock_count>max_count):
#         break
#     try:
#         count,page_count,stock_code=get_page_info(stock)
#         print("count:",count)
#         print("page_count:",page_count)
#         print("stock_code:",stock_code)
#     except Exception as e:
#         print(f"get_page_info error! stock:{stock}",e,flush=True)
#         continue
from utils import page_info_csv_file_path
def get_page_info_main(stocks):
    stock_count=0
    import concurrent.futures
    # 创建一个线程池，指定最大线程数为 3
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures=[]
        for stock in stocks:
            stock_count=stock_count+1
            if(max_count is not None and stock_count>max_count):
                break
            try:
                executor.submit(get_page_info,stock)
            except Exception as e:
                print(f"get_page_info error! stock:{stock}",e,flush=True)
                continue

        # 遍历 Future 对象，获取执行结果
        for future in concurrent.futures.as_completed(futures,timeout=60*60*24*7):
            try:
                result = future.result()
                print(result)
            except Exception as e:
                print(f"An error occurred: {e}")
    return page_info_csv_file_path

if __name__ == '__main__':
    pg=0
    stocks_df=pd.read_csv(f'divs/stocks_{pg}.csv')
    # 定义添加前缀和小写化的函数
    def add_prefix_and_lowercase(text, prefix):
        return prefix + text.lower()
    prefix = 'us'
    # 为某列添加前缀并将原文本小写化
    stocks_df['name_en'] = stocks_df['name_en'].apply(lambda x: add_prefix_and_lowercase(x, prefix))
    stocks=stocks_df['name_en'].tolist()
    page_info_csv_file_path=get_page_info_main(stocks)