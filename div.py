import pandas as pd

# 加载原始csv文件
df = pd.read_csv('stocks.csv')

# 选取name_en列中不包含"."或","的数据，创建新的数据框
new_df = df[~df['name_en'].str.contains('[\.,]')]

# 选取name_en列中包含数字的数据，创建新的数据框
new_df = new_df[~new_df['name_en'].str.contains('\d')]

print(new_df)

# 每个文件包含的行数
n=1000
# 按照行号进行分组
groups = new_df.groupby(new_df.index // n)

# 将分组后的数据块写入新的csv文件中
for i, group in groups:
    group.to_csv('stocks_{}.csv'.format(i), index=False)