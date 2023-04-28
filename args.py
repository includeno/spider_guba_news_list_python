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

from test_requests import main
df=pd.read_csv(f'divs/stocks_{args.stock}.csv')
stocks=df['name_en'].tolist()
page_info_csv_file_path=main(stocks)
#file_path=get_table(args.stock,args.max_page)

send_email(args.sender,args.ps,args.recipient,args.smtp_server,args.port,subject='GuBa News',attachment_path_list=[page_info_csv_file_path])
