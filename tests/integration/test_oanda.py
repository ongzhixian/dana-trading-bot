import json
import logging
import requests
import unittest


log = logging.getLogger()
for handler in log.handlers:
    log.removeHandler(handler)

#filter logging for import modules
#logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

logging_format = logging.Formatter('%(asctime)-15s.%(msecs)d %(levelname)-8s %(name)-5s %(message)s')
log.setLevel(logging.DEBUG)

console_logger = logging.StreamHandler()
console_logger.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d [%(levelname)-5s] %(message)s', datefmt="%H:%M:%S"))
log.addHandler(console_logger)

file_logger = logging.FileHandler('test_oanda.log')
file_logger.setFormatter(logging_format)
log.addHandler(file_logger)


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
    log.info(f"Trading using account_id: {account_id}")

    account_summary = get_account_summary(account_id)['account']
    margin_rate = account_summary['marginRate']
    balance = account_summary['balance']
    nav = account_summary['NAV']
    open_trade_count = account_summary['openTradeCount']
    open_position_count = account_summary['openPositionCount']
    pending_order_count = account_summary['pendingOrderCount']
    last_transaction_id = account_summary['lastTransactionID']

    log.info(f"margin_rate: {margin_rate}        balance: [{balance}]        nav: [{nav}]")
    log.info(f"open_trade_count: {open_trade_count}        open_position_count: {open_position_count}        pending_order_count: {pending_order_count}")

    
            
    

    # print(f"S: {s}")
    # account_instruments  == tradable instruments; which is why we don't see btc_usd (currently not tradable with tiny account)
    x = get_account_instruments(account_id)
    instruments = x['instruments']
    log.info(f"Number of instruments found: [{len(instruments)}]")

    instrument_types = {}

    # Write code 
    for instrument in instruments:
        instrument_type = instrument['type']
        if instrument_type in instrument_types:
            instrument_types[instrument_type] = instrument_types[instrument_type] + 1
        else:
            instrument_types[instrument_type] = 1
    for instrument_type in instrument_types:
        # CURRENCY : 69
        log.info(f"{instrument_type:>8} : {instrument_types[instrument_type]}")
    
    interested_instruments = ["XAU_USD", "EUR_USD", "USD_JPY", "SPX500_USD" "BTC_USD"]



    # print(x)

    # "EUR_USD:S10:BM"
    # any combination of the characters 'M' (midpoint candles) 'B' (bid candles) and 'A' (ask candles)
    c = get_candles_latest(account_id, "XAU_USD", "H1", "BM")
    print(c)
    
    # candle_specification_list = []
    # candle_specification_list.append(candle_specification("XAU_USD", "H1", "B"))
    # candle_specification_list.append(candle_specification("EUR_USD", "S10", "BM"))
    # x = candle_specification_list
    # ",".join(candle_specification_list)

    # import urllib3.parse.quote
    # import pdb
    # pdb.set_trace()
    # import urllib.parse
    # from urllib.parse import quote as url_encode
    #xxx = url_encode('zj@asd.zxc')
    # print(url_encode('zj@asd.zxc'))
    # print(url_encode(",".join(candle_specification_list)))