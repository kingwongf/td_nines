# First import the libraries that we need to use
import pandas as pd
import requests
import json

def fetch_daily_data(symbol):
    url = f'https://api.pro.coinbase.com/products/{symbol}/candles?granularity=86400'
    response = requests.get(url)
    if response.status_code == 200:  # check to make sure the response from server is good
        data = pd.DataFrame(json.loads(response.text), columns=['unix', 'Low', 'High', 'Open', 'Close', 'Volume'])
        data['Date'] = pd.to_datetime(data['unix'], unit='s')  # convert to a readable date
        data['vol_fiat'] = data['Volume'] * data['Close']      # multiply the BTC volume by closing price to approximate fiat volume

        # if we failed to get any data, print an error...otherwise write the file
        if data is None:
            print("Did not return any data from Coinbase for this symbol")
        else:
            symbol = symbol.replace("-","")
            data.to_csv(f'{symbol}.csv', index=False)
    else:
        print("Did not receieve OK response from Coinbase API")

for sym in ["BTC-GBP", "ETH-GBP", "LTC-GBP", "OMG-GBP", "NMR-GBP"]:
    df = fetch_daily_data(sym)
    # sym = sym.replace("-","")
    # df.to_csv(f"{sym}.csv")