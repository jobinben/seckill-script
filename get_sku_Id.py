import requests
import time


def getParam():
    header = {
    'Host': 'gkxy.tetele.net',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'content-type': 'application/json',
    'token': 'f52cb1b9-d9fc-45fd-808c-101923a9cfc6'}
    
    data = {"business_id": 0, "page_num": 1, "page_size": 20, "type": "home_recommend", "area_id": "", "subsite_id": ""}
    req = requests.post(url="https://gkxy.tetele.net/proapi/get_hot_recommend", headers=header, json=data)
    print(req)
    if req.status_code == 200:
        for i in req.json()['data']:
            int_time = time.localtime(int(i['StartSaleTime']))
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", int_time)
            product_time = time.strftime("%Y-%m-%d", int_time)
            today_time = time.strftime("%Y-%m-%d", time.localtime())
            if product_time == today_time:
                print(start_time, "sku_id：%s" % i['Skus'][0]['Id'], "product_id：%s" % i['Skus'][0]['ProductId'], i['Title'], "价格: %s" % i['Skus'][0]['DistributorPrice'])
                skuID = i['Skus'][0]['Id']
                proID = i['Skus'][0]['ProductId']
                return [skuID, proID]
        return False




