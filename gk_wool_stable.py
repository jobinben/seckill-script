import requests
import json
import time
from multiprocessing import Process
from os import getpid
from get_sku_Id import getParam


class Wool(object):

    def __init__(self, host, connection, platform, contentType, acceptEncoding, userAgent, token):
        self._host = host
        self._connection = connection
        self._platform = platform
        self._contentType = contentType
        self._acceptEncoding = acceptEncoding
        self._userAgent = userAgent
        self._token = token

    @property
    def Host(self):
        return self._host

    @property
    def connection(self):
        return self._connection
    @property
    def platform(self):
        return self._platform
    @property
    def contentType(self):
        return self._contentType
    @property
    def acceptEncoding(self):
        return self._acceptEncoding
    @property
    def userAgent(self):
        return self._userAgent
    @property
    def token(self):
        return self._token
    
    """获取头文件"""
    def getHeader(self):
        return {
            'Host': self._host,
            'Connection': self._connection,
            'platform': self._platform,
            'content-type': self._contentType,
            'Accept-Encoding': self._acceptEncoding,
            'User-Agent': self._userAgent,
            'token': self._token
        }


class User(Wool):
    """ 用户 """

    def __init__(self, address_id, book_name, book_phone, sku_id, product_id):
        """ 初始化

        :param token: 用户唯一标识符token

        :param address_id: 用户地址id

        :param book_name: 用户名

        :param book_phone: 用户电话

        :param sku_id: 商品副ID

        :param product_id: 商品ID

        """
        self._address_id = address_id
        self._book_name = book_name
        self._book_phone = book_phone
        self._sku_id = sku_id
        self._product_id = product_id

    @property
    def address_id(self):
        return self._address_id
    
    @property
    def book_name(self):
        return self._book_name
    @property
    def book_phone(self):
        return self._book_phone
    @property
    def sku_id(self):
        return self._sku_id
    @property
    def product_id(self):
        return self._product_id
    
    """获取data"""
    def getData(self):
        return {"address_id": self.address_id, "sku_id": self.sku_id, "quantity": "1", "product_id": self.product_id,
        "from": "miniapp", 'book_name': self.book_name, 'book_phone': self.book_phone}



# code 1000 下单成功， code 8413 已售完
# {"code":8413,"msg":"下单失败，每个用户只能购买1份"}
# {"code":10005,"msg":"已被抢完"}
# {"code":10002,"msg":"token错误"}

def go(data, header, name):
    count = 1
    session = requests.Session()  # 保存成功请求会话参数（例如cookie），便于发送请求
    while True:
        req = session.post(
            url='https://gkxy.tetele.net/orderapi/add', json=data, headers=header)
        req_json = json.loads(req.text)
        # print("#%s %s" % (name, count), req, req.text)
        count += 1
        h = time.strftime("%H",time.localtime())
        m = time.strftime("%M",time.localtime())
        s = time.strftime("%S",time.localtime())
        if req_json['code'] == 1000:
            data_1 = {"order_sn": req_json['order_sn'],
                        "pay_type": "miniapp", "pay_method": "wechat"}
            req_1 = session.post(
                url='https://gkxy.tetele.net/addons/xshop/pay', headers=header, json=data_1)
            print("#%s# -> " % name, req_1, req_1.text)
            session.close()
            break
        elif h=="12" and m >= "15":
            break
        elif req_json['code'] == 10002:
            print("#%s %s" % (name, count), req, req.text)
            break
        time.sleep(0.05)
    

def run_task(data,header,name):
        print('启动进程，进程号[%d].' % getpid())
        go(data, header, name)

def main():
    paramArr = getParam()
    print('paramArr=', paramArr)
    if not paramArr:
        print('无秒杀活动')
        return
    
    host = 'gkxy.tetele.net'
    connection = 'keep - alive'
    platform = 'MP-WEIXIN'
    contentType = 'application/json'
    acceptEncoding = 'gzip, compress, br, deflate'
    userAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.4(0x18000429) NetType/4G Language/zh_CN'
    sku_id = paramArr[0]
    product_id = paramArr[1]
    print(sku_id)

    # c6fa4ec0-17eb-4f17-9b39-e062611b5eac 周星星 false
    w1 = Wool(host, connection, platform, contentType, acceptEncoding, userAgent, 'a4b37e8c-3398-4b0b-a8d4-c508fd9a4bc1')
    u1 = User(2002, '周星星', '18927901200', sku_id, product_id)
   
    # 87607ac3-6ace-4776-a674-f219243f9a33 cure
    w2 = Wool(host, connection, platform, contentType, acceptEncoding, userAgent, '80f96861-9b9b-4169-9ffd-42a0b5b83782')
    u2 = User(419, 'cure', '18927900200', sku_id, product_id)

    # 48644b4d-b4c8-4075-91c3-781e4df85b17 小boy
    w3 = Wool(host, connection, platform, contentType, acceptEncoding, userAgent, '8b4c7e2f-7440-4d45-9173-22328885ca54')
    u3 = User(822, 'boy', '18927902200', sku_id, product_id)

    # f8b49974-4de6-461f-80d2-91354bee5af7 小哥
    w4 = Wool(host, connection, platform, contentType, acceptEncoding, userAgent, 'dc1ff5e0-e77d-4220-82d7-39ea97ae1a49')
    u4 = User(3, '哥哥', '18927903000', sku_id, product_id)

    # 16941b05-b8b4-4cde-a348-cb69e71956c2 小黑 1966
    w5 = Wool(host, connection, platform, contentType, acceptEncoding, userAgent, 'ccde9cdf-bfbb-4359-8f86-5c1a1372b4f1')
    u5 = User(1966, '小黑', '18927902000', sku_id, product_id)

    # 44b40899-c7a0-48ad-9a52-3fae011e1e4c jobin 1966
    w6 = Wool(host, connection, platform, contentType, acceptEncoding, userAgent, 'eda4826b-8834-4a0d-a8b4-745153fc1cac')
    u6 = User(1966, 'jobin', '18206607000', sku_id, product_id)

    # 执行
    start = time.time()
    p1 = Process(target=run_task, args=(u1.getData(), w1.getHeader() , u1.book_name,))
    p1.start()
    p2 = Process(target=run_task, args=(u2.getData(), w2.getHeader() , u2.book_name,))
    p2.start()
    p3 = Process(target=run_task, args=(u3.getData(), w3.getHeader() , u3.book_name,))
    p3.start()
    p4 = Process(target=run_task, args=(u4.getData(), w4.getHeader() , u4.book_name,))
    p4.start()
    p5 = Process(target=run_task, args=(u5.getData(), w5.getHeader() , u5.book_name,))
    p5.start()
    p6 = Process(target=run_task, args=(u6.getData(), w6.getHeader() , u6.book_name,))
    p6.start()
 
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()

    end = time.time()
    print('总共耗费了%.2f秒.' % (end -start))


# 定时开启任务
def settime(seth, setm, sets):
    print(time.strftime("%H:%M:%S",time.localtime()))

    while(1):
        h = time.strftime("%H",time.localtime())
        m = time.strftime("%M",time.localtime())
        s = time.strftime("%S",time.localtime())
        print(h,m,s)
        if(h==seth and m == setm and s == sets):
            print('go')
            main()
        time.sleep(1)
        


if __name__ == "__main__":
    settime("12", "09", "50")
    # main()

