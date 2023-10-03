import pandas as pd
import numpy as np
import sys,os,getopt,requests
from datetime import datetime

startTime = 1695945600000
endTime = 1696118400000
diffrece = endTime - startTime
print(diffrece)
print(f"{diffrece/86400000} days")

market = 'BTCUSDT'
tick_interval = '1h'  
url = f'https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1m&startTime={startTime}&endTime={endTime}&limit=1500'
data = np.array(requests.get(url).json())

datetime = pd.to_datetime(data[:,0].astype('int'),unit='ms',utc=True)
data = pd.DataFrame({"Open time": pd.to_datetime(data[:,0].astype('int'),unit='ms',utc=True),"Open":data[:,1], "High":data[:,2], "Low":data[:,3], "Close":data[:,4], "Volume":data[:,5], "Quote Volume":data[:,7], "Trade count":data[:,8],"Taker base volume":data[:,9], "Taker quote volume":data[:,10]})
data.to_csv("./test.csv")
"""
def main(argv):
    pair = ""
    start = ""
    end = ""
    timeframe = ""
    usage = "usage:\npython3 file.py [-h (help)] <-p asset pair> <-s start time> <-e end time> <-t candel timeframe>"
    help = f"help:\n-h --help, -p --pair, -s --start, -e --end, -t --timeframe\n{usage}\ne.g. python3 get_binance_timeseries.py -p BTCUSDT -s 10-01-2023 -e 10-02-2023 -t 1hour\n***You will need to use a vpn to use this program!***"


#use getopt to parse inline commands
    try:
        opts,args = getopt.getopt(argv[1:],"hp:s:e:t:",["help","pair=","start=","end=","timeframe="])
    except getopt.GetoptError:
        print(usage)
        sys.exit()
    
    #run through the options a nd set thier respected variables
    for opt, arg in opts:
        #print("opt",opt,"arg",arg)
        if opt in ("-h","--help"):
            print(help)
            sys.exit()
        elif opt in ("-p","--pair"):
            pair = arg
        elif opt in ("-s","--start"):
            start = arg
        elif opt in ("-e","--end"):
            end = arg 
        elif opt in ("-t","--timeframe"):
            timeframe = arg 

    #catch if any required variabls is are not set and set those the are optional that havent been set by the user to 0
    if((not pair)|(not start)|(not end)|(not timeframe)):
        print(f"Required option -p, -s, -e, or -t is empty.\n{help}")
        sys.exit()
    
    getTradeData(pair, start, end, timeframe)

main(sys.argv)
sys.exit()
"""
