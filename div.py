import pandas as pd
import os

divs_folder_path = "divs"

# 如果文件夹不存在，则创建文件夹
if not os.path.exists(divs_folder_path):
    os.makedirs(divs_folder_path)

# 加载原始csv文件
df = pd.read_csv('stocks.csv')

# 选取name_en列中不包含"."或","的数据，创建新的数据框
new_df = df[~df['name_en'].str.contains('[\.,]')]

# 创建新的数据框，包含不包含逗号、下划线或数字的名称
new_df = new_df[new_df['name_en'].str.match(r'^[a-zA-Z]+$')]

print(new_df)

# 每个文件包含的行数
n=200
# 按照行号进行分组
groups = new_df.groupby(new_df.index // n)

# 将分组后的数据块写入新的csv文件中
for i, group in groups:
    group.to_csv(os.path.join(divs_folder_path,'stocks_{}.csv'.format(i)), index=False)