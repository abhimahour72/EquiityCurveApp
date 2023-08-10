import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd
import math
import matplotlib.pyplot as plt
import datetime
import streamlit as st

st.title("Stocks App")

st.write("please wait while data is being downloaded from yahoo finance")
st.write("you can refresh the page if any error occurs")

st.subheader("")
st.write("start date = ", '2020-20-01')
st.write("end date = ", 'Current date')
st.write("investment = ", 1000000)
st.write("No of top performing stocks to be found = ", 10)

start_date = datetime.datetime(2020,10,1)
investment = 1000000
basic_stategy_units = 50
advance_strategy_units = 10

url = "https://en.wikipedia.org/wiki/NIFTY_50"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
table = soup.find('table', class_='wikitable sortable')
nifty50_sym = []
for row in table.find_all('tr')[1:]:
    company_sym = row.find_all('td')[1].text.strip()
    nifty50_sym.append(company_sym)
nifty50_sym = [i+".NS" for i in nifty50_sym]
joined_sym = " ".join(nifty50_sym)

All_data = yf.download(joined_sym,threads=True).dropna()
col = [("Open",sym) for sym in nifty50_sym] + [("Close",sym) for sym in nifty50_sym]
All_data = All_data[col]

indexForEmptyDF = [("Qty",sym) for sym in nifty50_sym] + [("Daily Value",sym) for sym in nifty50_sym] + [("Equity_curve","")]
emptyDF = pd.DataFrame(columns=indexForEmptyDF)
AllDataforNIFTY50 = pd.concat([All_data, emptyDF]).fillna(0)
AllDataforNIFTY50.index=pd.to_datetime(AllDataforNIFTY50.index)
AllDataforNIFTY50 = AllDataforNIFTY50[AllDataforNIFTY50.index >= start_date]

AllDataforNIFTY50['Qty'] = AllDataforNIFTY50['Qty'] + (investment/basic_stategy_units)/AllDataforNIFTY50["Open"].iloc[0]
AllDataforNIFTY50['Qty'] = AllDataforNIFTY50['Qty'].astype(int)
AllDataforNIFTY50['Daily Value'] = AllDataforNIFTY50['Daily Value'] + (AllDataforNIFTY50['Close']*AllDataforNIFTY50['Qty'])
AllDataforNIFTY50['Equity_curve']=AllDataforNIFTY50['Equity_curve']+AllDataforNIFTY50['Daily Value'].sum(axis=1)
st.subheader("Calculations for equal buy and hold(Benchmark Strategy)")
AllDataforNIFTY50




NoOfYears = len(AllDataforNIFTY50.index.year.unique().values)
CAGR_equalBuyHold = (((AllDataforNIFTY50['Equity_curve'][-1]/AllDataforNIFTY50['Equity_curve'][0])**(1/NoOfYears))-1)*100
# st.write("cagr_equal_buy_hold = ",CAGR_equalBuyHold)
dailyReturns_equal_buy_hold = ((AllDataforNIFTY50['Equity_curve']/AllDataforNIFTY50['Equity_curve'].shift(1))-1)
sharpe_ratio = (dailyReturns_equal_buy_hold.mean()/dailyReturns_equal_buy_hold.std())**(1/252)
# st.write("sharpe_ratio_equal_buy_hold = ",sharpe_ratio)
volatility_equal_buy_hold = ((dailyReturns_equal_buy_hold.std())**(1/252))*100
# st.write("volatility_equal_buy_hold",volatility_equal_buy_hold)

DataForAdvanceStrategy = All_data[All_data.index < start_date]
list_temp = DataForAdvanceStrategy['Close'].iloc[-1]/DataForAdvanceStrategy['Close'].iloc[-100]-1
listOfTopPerformers=list_temp.sort_values(ascending=False).index[:10].to_list()
st.subheader("list of top 10 stocks selected")
st.write(pd.DataFrame(listOfTopPerformers).transpose())
st.subheader("")
colTupleForPerfStrategy = [("Open",sym) for sym in listOfTopPerformers]+[("Close",sym) for sym in listOfTopPerformers]
perf_data=All_data[colTupleForPerfStrategy]
indexForEmptyDF_2 = [("Qty",sym) for sym in listOfTopPerformers] + [("Daily Value",sym) for sym in listOfTopPerformers] + [("Equity_curve","")]
emptyDF = pd.DataFrame(columns=indexForEmptyDF_2)
perf_data10 = pd.concat([perf_data, emptyDF]).fillna(0)
perf_data10.index=pd.to_datetime(perf_data10.index)
perf_data10 = perf_data10[perf_data10.index >= start_date]
perf_data10['Qty'] = perf_data10['Qty'] + (investment/advance_strategy_units)/perf_data10["Open"].iloc[0]
perf_data10['Qty'] = perf_data10['Qty'].astype(int)
perf_data10['Daily Value'] = perf_data10['Daily Value'] + (perf_data10['Close']*perf_data10['Qty'])
perf_data10['Equity_curve']=perf_data10['Equity_curve']+perf_data10['Daily Value'].sum(axis=1)
st.subheader("Calculations for Sample strategy (Past return based selection)")

perf_data10

NoOfYears_perf = len(perf_data10.index.year.unique().values)
CAGR_perf = (((perf_data10['Equity_curve'][-1]/perf_data10['Equity_curve'][0])**(1/NoOfYears_perf))-1)*100
# st.write("cagr_perf = ",CAGR_perf)
dailyReturns_perf = ((perf_data10['Equity_curve']/perf_data10['Equity_curve'].shift(1))-1)
sharpe_ratio_perf = (dailyReturns_perf.mean()/dailyReturns_perf.std())**(1/252)
# st.write("sharpe_ratio_perf = ",sharpe_ratio_perf)
volatility_perf = ((dailyReturns_perf.std())**(1/252))*100
# st.write("volatility_perf",volatility_perf)



data_NSEI = yf.download("^NSEI",start="2020-10-01",threads=True)
data_NSEI.rename_axis(None,inplace=True)
NSEI_indexColTuple = [("Open","NSEI"),
       ("High","NSEI"),
       ("Low","NSEI"),
       ("Close","NSEI"),
       ("Adj Close","NSEI"),
       ("Volume","NSEI")]

data_NSEI.columns = pd.MultiIndex.from_tuples(NSEI_indexColTuple)
data_NSEI = data_NSEI[["Open","Close"]]
emop_df = [("Qty","NSEI"),
           ("Daily Value","NSEI"),
           ("Equity_curve","")]
edsdd = pd.DataFrame(columns=emop_df)
data_NSEI_new = pd.concat([data_NSEI,edsdd]).fillna(0)
data_NSEI_new['Qty']= data_NSEI_new['Qty'] + investment/data_NSEI_new['Open'].iloc[0]
data_NSEI_new['Qty']=data_NSEI_new['Qty'].astype(int) 
data_NSEI_new['Daily Value'] = data_NSEI_new['Daily Value'] + (data_NSEI_new['Qty']*data_NSEI_new['Close'])
data_NSEI_new['Equity_curve'] = data_NSEI_new['Equity_curve'] + data_NSEI_new['Daily Value','NSEI']
st.subheader("Calculations for nifty index strategy")

data_NSEI_new


NoOfYears_index = len(data_NSEI_new.index.year.unique().values)
CAGR_NSEI = (((data_NSEI_new['Equity_curve'][-1]/data_NSEI_new['Equity_curve'][0])**(1/NoOfYears_index))-1)*100
# st.write("cagr_NSEI = ",CAGR_NSEI)
dailyReturns_index = ((data_NSEI_new['Equity_curve']/data_NSEI_new['Equity_curve'].shift(1))-1)
sharpe_ratio_index = (dailyReturns_index.mean()/dailyReturns_index.std())**(1/252)
# st.write("sharpe_ratio_index = ",sharpe_ratio_index)
volatility_index = ((dailyReturns_index.std())**(1/252))*100
# st.write("volatility_index",volatility_index)
st.subheader("")
st.header("Equity curve")
st.line_chart({"Nifty_index":data_NSEI_new['Equity_curve'],"Performance_strategy":perf_data10['Equity_curve'],"Equal Alloc Buy Hold":AllDataforNIFTY50['Equity_curve']})

dictt = {"Index":["Equal Alloc Buy Hold","Nifty","Performace_stratagy"],
         "CAGR%":[CAGR_equalBuyHold,CAGR_NSEI,CAGR_perf],
         "Volatility%":[volatility_equal_buy_hold,volatility_index,volatility_perf],
         "Sharpy":[sharpe_ratio,sharpe_ratio_index,sharpe_ratio_perf]}
frame = pd.DataFrame(dictt)
frame.set_index("Index",inplace=True)
st.subheader("")
st.subheader("Performance Matrix")
st.dataframe(frame)