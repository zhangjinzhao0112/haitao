import requests
import json
import xlsxwriter
import os
import time

# 需要登录之后获取token
# column_count指要最近的多少条数据
jwt_token = ''
column_count = '1000'

url = 'https://mec.yto.net.cn/api/order/searchOrderList?limit={}&pageNo=1&flag=0'.format(column_count)
headers = {'Host': 'mec.yto.net.cn', 'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
           'content-type': 'application/json;charset=UTF-8', 'Accept-Encoding': 'gzip, deflate, br',
           'jwt-token': jwt_token}

response = requests.get(url, headers=headers)
data = response.text
data = json.loads(data)
items = data['items']

result_list = []
for item in items:
    print(item)
    result = {
        'source': item['source'],
        'order_no': item['orderNo'],
        'mail_no': item['mailNo'] if 'mailNo' in item.keys() else '',
        'receiver_name': item['receiverName'],
        'receiver_phone': item['receiverPhone'],
        'receiver_province_name': item['receiverProvinceName'],
        'receiver_city_name': item['receiverCityName'],
        'sender_name': item['senderName'],
        'sender_phone': item['senderPhone'],
        'sender_province_name': item['senderProvinceName'],
        'sender_city_name': item['senderCityName'],
        'status_name': item['statusName'],
        'create_time': item['createTime']
    }
    result_list.append(result)

prefix = 'output/'
if not os.path.exists(prefix):
    os.makedirs(prefix)
    print('目录创建成功')
current_date = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
excel = xlsxwriter.Workbook(prefix + '圆通' + current_date + '.xlsx')
sheet = excel.add_worksheet('快递信息')

titles = ['来源', '订单号', '快递单号', '收件人', '收件人手机号', '收件人省份', '收件人城市',
          '寄件人', '寄件人手机号', '寄件人省份', '寄件人城市', '订单状态', '创建时间']
title_keys = ['source', 'order_no', 'mail_no', 'receiver_name', 'receiver_phone', 'receiver_province_name',
              'receiver_city_name', 'sender_name', 'sender_phone', 'sender_province_name', 'sender_city_name',
              'status_name', 'create_time']

for i in range(0, len(titles)):
    sheet.write(0, i, titles[i])

column_count = 0
for i in range(0, len(result_list)):
    if column_count != 0:
        column_count = 0
    for key in title_keys:
        sheet.write(i + 1, column_count, result_list[i].get(key))
        column_count = column_count + 1
excel.close()


# print('start to insert mongo')
# client = mongotool.get_mongo_client()
# db = client[constant.mongo_db_name]
# yto_collection = db[constant.express_collection]
#
# # 先查,根据order_no分为需要直接插入和更新的
# order_no_list = [x['order_no'] for x in result_list]
# yto_docs = yto_collection.find({'order_no': {'$in': order_no_list}})
# mongo_order_no_list = [x['order_no'] for x in yto_docs]
#
# insert_list = []
# update_list = []
# for r in result_list:
#     if r['order_no'] in mongo_order_no_list:
#         update_list.append(r)
#     else:
#         insert_list.append(r)
#
# yto_collection.insert_many(insert_list)
# for u in update_list:
#     yto_collection.update_one({'order_no': u['order_no']}, {'$set': {'status_name': u['status_name']}})
#
# client.close()
