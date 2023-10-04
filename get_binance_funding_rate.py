import pandas as pd
import numpy as np
import sys,os,getopt,requests
from datetime import datetime

#startTime = 1693526400000 - (2629743000 * 5)
#endTime = 1696118400000 - (2629743000 * 5)

startTime = 1659312000000
endTime = 1664582400000
print(pd.to_datetime(endTime,unit='ms'))
print(pd.to_datetime(startTime,unit='ms'))
url = f'https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&startTime={startTime}&endTime={endTime}&limit=1000'
new_data = np.array(requests.get(url).json())
print(new_data)
print(len(new_data))
pd.DataFrame(list(new_data)).to_csv("./Aug2022-Oct2022-funding-fees.csv")
"""
run = 3
old_data = []
while(run):
    url = f'https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&startTime={startTime}&endTime={endTime}&limit=1000'
    new_data = np.array(requests.get(url).json())
    if(not data):
        run = 0
    startTime = data[0]['fundingTime'] - 2629743000
    endTime = data[0]['fundingTime']
    old_data.append(new_data)
    run--

print()
"""
#print(pd.to_datetime(data[0]['fundingTime'],unit='ms'))
#print(pd.to_datetime(data[len(data)-1]['fundingTime'],unit='ms'))
    #fundingTime = [pd.to_datetime(item['fundingTime'],unit='ms',utc=True) for item in data]
    #print(fundingTime)

#datetime = pd.to_datetime(data[:,0].astype('int'),unit='ms',utc=True)
#data = pd.DataFrame({"Symbol": data[:,0],"Open":data[:,1], "High":data[:,2], "Low":data[:,3], "Close":data[:,4], "Volume":data[:,5], "Quote Volume":data[:,7], "Trade count":data[:,8],"Taker base volume":data[:,9], "Taker quote volume":data[:,10]})
#data.to_csv("./test.csv")
