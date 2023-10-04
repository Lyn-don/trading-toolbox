import vectorbtpro as vbt
import os,getopt,sys

def getTradeData(pair, start, end, timeframe):
    vbt.BinanceData.set_custom_settings(
    client_config=dict(tld="us"
    )
)
    # Get the data
    data = vbt.BinanceData.fetch(pair, start=start, end=end, timeframe=timeframe)
   
    timeframe = timeframe.replace(" ","")
    # Make dir recurivly
    if(os.path.exists(f"./data/datasets/{timeframe}")):
        print("Hello!")
        os.makedirs(f"./data/datasets/{timeframe}")

    #save data in gerated folder
    data.to_csv(path_or_buf=f'./data/datasets/{pair}/{timeframe}/{pair}_{start}_to_{end}_{timeframe}.csv',mkdir_kwargs=dict(mkdir=True))
    
    print(f'file is at ./data/datasets/{timeframe}/{pair}_{start}_to_{end}_{timeframe}.csv')

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
