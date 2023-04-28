import argparse
import datetime
from spider import get_table
from mail_sender import send_email
import pandas as pd

def today():
    today = datetime.datetime.today()
    date_string = today.strftime('%Y-%m-%d')
    print(date_string)
    return date_string

# 创建 ArgumentParser 对象，用于处理命令行参数
parser = argparse.ArgumentParser(description='一个简单的命令行接口示例')

# 添加命令行参数
#email
parser.add_argument('--sender',required=True, help='输入发送邮箱')
parser.add_argument('--ps',required=True, help='输入邮箱密码')
parser.add_argument('--recipient',required=True, help='输入收件人邮箱')
parser.add_argument('--smtp_server',required=True, help='输入smtp_server')
parser.add_argument('--port',required=True, help='输入smtp_server的端口')

parser.add_argument('--stock',required=True, help='输入爬取的stock 序号')
parser.add_argument('--max_page',required=False,default=None, help='输入爬取的最大页数')
# 解析命令行参数
args = parser.parse_args()

# 将版本号写入文件
with open('DATE', 'w') as f:
    f.write(f'DATE={today()}\n')

from get_all_stock_page_info_concurrent import get_page_info_main
stocks_df=pd.read_csv(f'divs/stocks_{args.stock}.csv')
# 定义添加前缀和小写化的函数
def add_prefix_and_lowercase(text, prefix):
    return prefix + text.lower()
prefix = 'us'
# 为某列添加前缀并将原文本小写化
stocks_df['name_en'] = stocks_df['name_en'].apply(lambda x: add_prefix_and_lowercase(x, prefix))
stocks=stocks_df['name_en'].tolist()
try:
    get_page_info_main(stocks)
except Exception as e:
    print("get_page_info_main error",e,flush=True)
#file_path=get_table(args.stock,args.max_page)
from utils import page_info_csv_file_path

send_email(args.sender,args.ps,args.recipient,args.smtp_server,args.port,subject='GuBa News',attachment_path_list=[page_info_csv_file_path])
