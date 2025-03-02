# import os
# import pandas as pd
#
# # 设置文件夹路径
# folder_path = './蔬菜价格'
#
# # 获取文件夹中所有csv文件的文件名列表
# file_names = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
#
# # 初始化一个空的DataFrame用于存储所有数据
# merged_data = pd.DataFrame()
#
# # 遍历所有csv文件，逐个读取并合并数据
# for file_name in file_names:
#     file_path = os.path.join(folder_path, file_name)
#     data = pd.read_csv(file_path)
#     merged_data = pd.concat([merged_data, data], ignore_index=True)
#
# # 对合并后的数据按照日期列进行升序排序
# merged_data_sorted = merged_data.sort_values(by=['发布日期', '品名'])
#
# # 去除相同日期和品名的重复行，保留第一次出现的行
# merged_data_sorted_unique = merged_data_sorted.drop_duplicates(subset=['发布日期', '品名'], keep='first')
#
# # 将排序后并去重后的数据保存为新的CSV文件
# merged_data_sorted_unique.to_csv('middle/merged_data_sorted_unique.csv', index=False)




import pandas as pd

filename = 'middle/merged_data_sorted_unique.csv'
data = pd.read_csv(filename, encoding='utf-8')

# 确定一共有多少种农产品
product_names = data[u'品名'].unique()
print("共有" + str(len(product_names)) + "种农产品")
print("分别是：", product_names)

# 根据农产品名称拆分数据并保存到单独的文件
for product_name in product_names:
    product_data = data[data[u'品名'] == product_name]
    file_out = "./农产品价格情况/" + product_name + '价格.csv'
    product_data.to_csv(file_out, index=False, encoding='utf-8')

#
