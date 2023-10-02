import sys,getopt,os
from pandas.core import resample
from lightweight_charts import Chart
import pandas as pd
import numpy as np

def main (argv):
    filename = ""
    save_dir = ""
    dataset_dir = ""
    timeframes = []
    dataset_range = []
    dataset_split = 1
    usage = "usage: python3 file.py [-h (help)] <-d dataset_dir> <-s save_dir> <-f filename> <-t timeframe> [-r dataset_range] [-a dataset_split]"
    help = "Options:\nOptinal:\n-h --help print out the usage more verbosely then close the program.\n-r --dataset_range The range of the dataset to use in the bachtest. Provide 2 numbers serseperated by , e.g. 0,1002\n-a --dataset_split divied the dataset by the set ammount and use each chunk on their own.\nRequired:\n-d --dataset_dir Where the csv that the hold the historical data is located\n-f --filename set the base name of the files which will contain the results of the backtest\n-s --save_dir where the backtest result will e loacted after completion.\n-t --timeframes A array of diffrent timeframes to set the dataset. The opperands need to be a larger timeframe the timeframe the dataset is. seperate the diffrent opperands with a , e.g. 1min,2hour,4month,5sec\n"
    #use getopt to parse inline commands
    try:
        opts,args = getopt.getopt(argv[1:],"hd:s:t:r:a:f:",["help","dataset_dir=","save_dir=","timeframes=","dataset_range=","dataset_split=","filename="])
    except getopt.GetoptError:
        print(usage)
        sys.exit()
    
    #run through the options a nd set thier respected variables
    for opt, arg in opts:
        #print("opt",opt,"arg",arg)
        if opt in ("-h","--help"):
            print(help)
            sys.exit()
        elif opt in ("-f","--filename"):
            #checks if the user also added a file type to the filename
            #if so then remove it
            if(arg.split(".")[1]):
                arg = arg.split(".")[0]
            filename = arg
        elif opt in ("-d","--dataset_dir"):
            dataset_dir = arg
        elif opt in ("-s","--save_dir"):
            save_dir = arg 
        elif opt in ("-t","--timeframes"):
            timeframes = arg.split(",") 
        elif opt in ("-r","--dataset_range"):
            dataset_range = arg.split(",")  
        elif opt in ("-a","--dataset_split"):
            arg = int(arg)
            if(arg <1):
                arg = 1
                print('Input for -a of --dataset_split was less then 1 so the dataset split amount will be set to 1.')
            dataset_split = arg

    print("Program is runnig with these params:","save_dir=",save_dir,"dataset_dir=",dataset_dir,"timestamp=",timeframes,"dataset_range=",dataset_range,"dataset_split=",dataset_split,"\n")
    
    #catch if any required variabls is are not set and set those the are optional that havent been set by the user to 0
    if((not dataset_dir)):
        print("Required options are empty.")
        sys.exit()
    if(not filename):
        dataset_name = dataset_dir.split('/')[len(dataset_dir.split('/'))-1]
        filename = dataset_name.split(".")[0]
    
    #run the actual program

    if(save_dir):
        if(not os.path.exists(save_dir)):
            os.makedirs(save_dir)
    
    #get the csv 
    ohlc_df = pd.read_csv(dataset_dir )
    #extract the first 5 columns which should be time,open,high,low,close
    ohlc_df = ohlc_df.iloc[:,:6]
    #rename the columns to standerdize them
    ohlc_df = ohlc_df.rename(columns={list(ohlc_df)[0]:"time",list(ohlc_df)[1]:"open",list(ohlc_df)[2]:"high",list(ohlc_df)[3]:"low",list(ohlc_df)[4]:"close",list(ohlc_df)[5]:"volume"})
    #set the first column which should be time as the index
    ohlc_df = ohlc_df.set_index(list(ohlc_df)[0])
    #convert the first row to datetime objects
    ohlc_df.index = pd.to_datetime(ohlc_df.index)
 
    if dataset_range:
        ohlc_df = ohlc_df[dataset_range[0]:dataset_range[1]]
   
    #print(type(pd.infer_freq(ohlc_df.index)))
    if(not timeframes):
        tf =pd.infer_freq(ohlc_df.index)
        timeframes.append(str(tf))
    
    #this cuts up the one dataframe evenly into an array of dataframes
    ohlc_df_arr = np.split(ohlc_df,dataset_split)

    #print(ohlc_df_arr)
    #print(ohlc_df_arr[0])
    #print(pd.infer_freq(ohlc_df_arr[0].index))
     
    #iterate ovet the 
    for ohlc in ohlc_df_arr:
        for timeframe in timeframes:
            print(timeframe)
            print(ohlc)
            resample_df = ohlc.resample(timeframe).first()
            #print(resample_df)
            #graph data
            """
            #make a subplots the graph multiple graphs on one html file
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), 
                        row_width=[0.2,0.7])
            #plot the candlesticks
            fig.add_trace(go.Candlestick(x=resample_df.index,open=resample_df['Open'],high=resample_df['High'],low=resample_df['Low'],close=resample_df['Close']),row=1,col=1);
            #remove the range slider the comes with the candlestick graph by default
            fig.update_layout(xaxis_rangeslider_visible=False)
            # Bar trace for volumes on 2nd row without legend
            fig.add_trace(go.Bar(x=resample_df.index, y=resample_df['Volume'], showlegend=True), row=2, col=1)
            
            #show graph by opening a borwser
            fig.show()
            """ 
            chart = Chart()
            chart.set(resample_df)

            chart.show(block=True)
            #save the graph
            if(save_dir):
                print(os.path.exists(f"./bean/BTCUSDT_2023-05-01_2023-06-01_5 min.html"))
                print(f"./bean/BTCUSDT_2023-05-01_2023-06-01_5 min.html")
                 
                print(os.path.exists(f"{save_dir}/{filename}"))
                print(f"{save_dir}/{filename}")
                  
                if(os.path.exists(f"{save_dir}/{filename}.html")):

                    print(f"{save_dir}/{filename}.html")

                    res = ""
                    while((not res == "n")or(not res == "y")):
                        res = input(f"The file \'{filename}\' in \'{save_dir}\' all ready exist do you want to over ride it?(n/y)")

                        if(res == "y"):
                            print("Nan")
                        elif(res == "n"):
                            print("Skipping file.")

if __name__ == '__main__':
    main(sys.argv)
    exit()


