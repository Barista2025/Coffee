import requests
import os
import datetime
import yfinance as yf
import json

def obtain_access_token():
    file = open("access_token.txt", "r")
    return file.readline().strip()

def obtain_hash_value(access_token):
    res = account_number(access_token).json()[0]
    return res["hashValue"]

def account_number(access_token):
    return requests.get(f'https://api.schwabapi.com/trader/v1/accounts/accountNumbers',
                           headers={'Authorization': f'Bearer {access_token}'}
                       )

def quotes(symbol, access_token):
    return requests.get(f'https://api.schwabapi.com/marketdata/v1/'+symbol+'/quotes',
                       headers={'Authorization': f'Bearer {access_token}'},
                       params={'fields': 'quote'}
                       ).json()[symbol]['quote']['askPrice']
def orderJson(stock,qn,qn_type,operation,p1):
    order = { 
         "orderType": "LIMIT",
         "session": "NORMAL",
         "duration": "DAY",
         "price": p1,
         "orderStrategyType": "SINGLE",
         "orderLegCollection":
         [   
             {   
                 "instruction": operation,
                 "quantity": qn, 
                 "quantityType": qn_type,
                 "instrument":
                 {   
                     "symbol": stock,
                     "assetType": "EQUITY"
                 }   
             }   
         ]   
    }   
    return order

def orderJson2(stock,qn,qn_type,operation,p1,p2):
    order = {
         "orderType": "LIMIT",
         "session": "NORMAL",
         "duration": "DAY",
         "orderStrategyType": "SINGLE",
         "orderLegCollection":
         [
             {
                 "instruction": operation,
                 "quantity": qn,
                 "quantityType": qn_type,
                 "instrument":
                 {
                     "symbol": stock,
                     "assetType": "EQUITY"
                 }
             }
         ]
    }
    return order

def order_place(accountHash, order, access_token):
    return requests.post(f'https://api.schwabapi.com/trader/v1/accounts/{accountHash}/orders',
                       headers={"Accept": "application/json",'Authorization': f'Bearer {access_token}',"Content-Type": "application/json"},
                       json=order, timeout=15
                       )
def get_order_status(order_id,access_token,accountHash):
    url = f"https://api.schwabapi.com/trader/v1/accounts/{accountHash}/orders/{order_id}"
    res = requests.get(url,headers={"Accept": "application/json",'Authorization': f'Bearer {access_token}'})
    return res.json()

def check_order_status2(order_id,access_token,accountHash):
    while True:
        url = f"https://api.schwabapi.com/trader/v1/accounts/{accountHash}/orders/{order_id}"
        res = requests.get(url,headers={"Accept": "application/json",'Authorization': f'Bearer {access_token}'})
        if res.status_code != 200:
            print("查詢失敗：", res.text)
            break
        status = res.json().get("status")
        if status == "FILLED":
            price = res.json()['orderActivityCollection'][0]['executionLegs'][0]['price']
            quantity = res.json()['orderActivityCollection'][0]['executionLegs'][0]['quantity']
            return price,quantity
    return 0,0

def cancel_order(accountHash, access_token, order_id):
    url = f"https://api.schwabapi.com/trader/v1/accounts/{accountHash}/orders/{order_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    res = requests.delete(url, headers=headers)
    if res.status_code == 200:
        print(f"Order {order_id} cancelled successfully.")
        return True
    else:
        print(f"Cancel order failed: {res.status_code} {res.text}")
        #infoirm human to take actions
        return False

def place_limit_order(symbol,budget,access_token,hashValue,operation):
    timeout=60
    poll_interval=5
    price = quotes(symbol,access_token)
    print(symbol+" "+str(price))
    qn = 1
    if operation == 'BUY':
        p1 = round(price*1.01,2)
        qn = budget // p1
    else:
        p1 = round(price*0.99,2)
        qn = budget
    order_response = order_place(hashValue,orderJson(symbol,qn,'SHARES',operation,p1),access_token)
    if not order_response:
        print(order_response.text)
        return 0,0

    order_id = order_response.headers['Location'].split('/')[-1]
    print(order_id)
    if not order_id:
        print("沒有取得orderId")
        return 0,0

    elapsed = 0
    while elapsed < timeout:
        status_resp = get_order_status(order_id,access_token,hashValue)
        if status_resp:
            status = status_resp.get("status")
            print(f"訂單狀態: {status} {status_resp}")
            if status == "FILLED":
                print("訂單已成交")
                price = status_resp['orderActivityCollection'][0]['executionLegs'][0]['price']
                quantity = status_resp['orderActivityCollection'][0]['executionLegs'][0]['quantity']
                return price,quantity
            elif status in ["CANCELED", "REJECTED", "EXPIRED"]:
                print(f"訂單狀態為終止狀態：{status}")
                return 0,0
        time.sleep(poll_interval)
        elapsed += poll_interval

    # 超時仍未成交，取消訂單
    print(f"超過{timeout}秒，訂單未成交，嘗試取消訂單...")
    cancel_order(account_hash, access_token, order_id)
    return 0,0

def place_buy_order(symbol,budget,access_token,hashValue):
    price = quotes(symbol,access_token)
    print(price)
    p1 = min(price+0.1,price*1.005)
    p2 = min(price+0.2,price*1.01)
    response = order_place(hashValue,orderJson(symbol,budget // p2,'SHARES','BUY',p1,p2),access_token)
    if response.status_code == 201:
        order_id = response.headers['Location'].split('/')[-1]
        price,quantity = check_order_status(order_id,access_token,hashValue)
        return price,quantity
    return 0,0

def place_sell_order(symbol,share,access_token,hashValue):
    price = quotes(symbol,access_token)
    print(price)
    p1 = price*0.99
    p2 = price*1.1
    response = order_place(hashValue,orderJson(symbol,share,'SHARES','SELL',p1,p2),access_token)
    if response.status_code == 201:
        order_id = response.headers['Location'].split('/')[-1]
        price,quantity = check_order_status(order_id,access_token,hashValue)
        return price,quantity
    return 0,0
