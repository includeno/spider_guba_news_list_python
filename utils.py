import json
import os
import pandas as pd

# 要创建的文件夹路径
json_folder_path = "json"
csv_folder_path = "csv"

# 如果文件夹不存在，则创建文件夹
if not os.path.exists(json_folder_path):
    os.makedirs(json_folder_path)
if not os.path.exists(csv_folder_path):
    os.makedirs(csv_folder_path)

def write_json(json_str,filename="data.json"):
    # 将JSON格式字符串解析为Python对象
    data = json.loads(json_str)
    return write_json_data(data,filename)

def write_json_data(data,filename="data.json"):
    # 将Python对象写入文件 将Python字典对象转换为JSON字符串，并指定ensure_ascii=False
    with open(os.path.join(json_folder_path,filename), 'w',encoding='utf-8') as f:
        json.dump(data, f,ensure_ascii=False)
    print(f"json {filename}写入成功",flush=True)
    return True

# result.append({"title":item["post_title"],"id":item["post_id"],"username":item["user_nickname"],"user_id":item["user_id"],"comment_count":item["post_comment_count"],"time":item["post_publish_time"]})
def write_page_csv_data(result_list,stock,page):
    df = pd.DataFrame(result_list, columns=['id','title','time','username','user_id','comment_count','stock','stockbar_name'])
    # 写入page的csv文件
    page_csv_file=f"links_guba_{stock}_{page}.csv"
    page_csv_file_path=os.path.join(csv_folder_path,page_csv_file)
    df.to_csv(page_csv_file_path,index=False)
    print(f"csv stock:{stock} page:{page}写入成功",flush=True)
    return page_csv_file_path

def write_merged_csv_data(result_list,stock):
    df = pd.DataFrame(result_list, columns=['id','title','time','username','user_id','comment_count','stock','stockbar_name'])
    #仅写入评论数量>1的数据
    merged_csv_file=f"links_guba_{stock}.csv"
    merged_csv_file_path=os.path.join(csv_folder_path,merged_csv_file)
    try:
        csv_df=pd.read_csv(merged_csv_file_path,encoding='utf-8')
        csv_df=pd.concat([csv_df,df],ignore_index=True)
        csv_df.drop_duplicates(subset=['id'],keep='last',inplace=True)
        csv_df.to_csv(merged_csv_file_path)
        print(f"csv stock:{stock} 合并成功",flush=True)
    except Exception as e:
        print("exception:",e)
        df.to_csv(merged_csv_file_path,index=False,encoding='utf-8')
        print(f"csv stock:{stock} 新建成功",flush=True)
    return merged_csv_file_path