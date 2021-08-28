import unittest
import requests
import json

def get_oanda_practice_account_settings():
    with open('app-secrets.json', 'r') as secrets_file:
        secrets_json = json.loads(secrets_file.read())
        accounts = secrets_json['oanda']['accounts']
        for account in accounts:
            if account['accountName'] == "practice":
                return account
        return None


def get_accounts():
    methodName = "/v3/accounts"
    api_url = f"{base_api_url}{methodName}"
    message_headers =  {
        "Authorization" : f"Bearer {base_api_key}",
        "Content-Type" : "application/json",
    }
    response = requests.get(api_url, headers=message_headers)
    return response.json()['accounts']


def get_practice_mt4_account_id():
    accts = get_accounts()
    for acct in accts:
        if 'MT4' in acct['tags']:
            return acct['id']
    

def get_account_summary(account_id):
    methodName = f"/v3/accounts/{account_id}/summary"
    api_url = f"{base_api_url}{methodName}"
    message_headers =  {
        "Authorization" : f"Bearer {base_api_key}",
        "Content-Type" : "application/json",
    }
    response = requests.get(api_url, headers=message_headers)
    return response.json()


def get_account_instruments(account_id):
    methodName = f"/v3/accounts/{account_id}/instruments"
    api_url = f"{base_api_url}{methodName}"
    message_headers =  {
        "Authorization" : f"Bearer {base_api_key}",
        "Content-Type" : "application/json",
    }
    response = requests.get(api_url, headers=message_headers)
    return response.json()



def get_candles_latest(account_id, instrument_name, candlestick_granularity, pricing_component):
    # 1) InstrumentName 2) CandlestickGranularity 3) PricingComponent
    # PricingComponent: any combination of the characters 'M' (midpoint candles) 'B' (bid candles) and 'A' (ask candles)
    # "EUR_USD:S10:BM"
    candle_specification = f"{instrument_name}:{candlestick_granularity}:{pricing_component}"
    methodName = f"/v3/accounts/{account_id}/candles/latest?candleSpecifications={candle_specification}"
    api_url = f"{base_api_url}{methodName}"
    message_headers =  {
        "Authorization" : f"Bearer {base_api_key}",
        "Content-Type" : "application/json",
    }
    response = requests.get(api_url, headers=message_headers)
    return response.json()


def xx():
    #getAccount
    methodName = "/v3/accounts"
    api_url = f"{base_api_url}{methodName}"
    message_headers =  {
        "Authorization" : f"Bearer {base_api_key}",
        "Content-Type" : "application/json",
        
    }
    # message_body = json.dumps({
    #     "chat_id" : chat_id,
    #     "text" : message
    # })
    #response = requests.post(api_url, headers=message_headers, data=message_body)
    response = requests.get(api_url, headers=message_headers)
    response.json()

def candle_specification(instrument_name, candlestick_granularity, pricing_component):
    return f"{instrument_name}:{candlestick_granularity}:{pricing_component}"

if __name__ == "__main__":
    pass
    account_info = get_oanda_practice_account_settings()
    base_api_url =  account_info['restApiUrl']
    base_account_number = account_info['accountNumber']
    base_api_key = account_info['apiKey']

    account_id = get_practice_mt4_account_id()
    print(account_id)

    s = get_account_summary(account_id)

    x = get_account_instruments(account_id)
    print(x)

    # "EUR_USD:S10:BM"
    # any combination of the characters 'M' (midpoint candles) 'B' (bid candles) and 'A' (ask candles)
    get_candles_latest(account_id, "XAU_USD", "H1", "BM")
    candle_specification_list = []
    candle_specification_list.append(candle_specification("XAU_USD", "H1", "B"))
    candle_specification_list.append(candle_specification("EUR_USD", "S10", "BM"))
    x = candle_specification_list
    ",".join(candle_specification_list)
    # import urllib3.parse.quote
    # import pdb
    # pdb.set_trace()
    import urllib.parse
    from urllib.parse import quote as url_encode
    #xxx = url_encode('zj@asd.zxc')
    print(url_encode('zj@asd.zxc'))
    print(url_encode(",".join(candle_specification_list)))