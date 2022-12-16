import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import yfinance as yf
import tkinter as tk
st_name = input().upper()

start_date = input()
end_date = input()

select = input().capitalize()
plt.style.use("fivethirtyeight")
def find_st(name , started, ended):
    if started == "" and ended == "":
        st_use = yf.download(name)
    elif started == "":
        st_use = yf.download(name, start = None ,end= ended)
    elif ended == "":
        st_use = yf.download(name, start= started, end = None)
    else:
        st_use = yf.download(name, start= started, end=ended)
    return st_use

st_used = find_st(st_name , start_date, end_date)

#MACD Siganl
def caculate(name,name_label):
    global macd,signal
    short = name.Close.ewm(span = 12, adjust = False).mean()
    long = name.Close.ewm(span = 26, adjust = False).mean()
    macd = short - long
    signal = macd.ewm(span = 9, adjust = False).mean()
def calculate_plot():
    plt.figure(figsize=(12.2,4.5))
    macd.plot(label = "MACD", color = "green")
    signal.plot(label = "Signal", color = "black")
    plt.legend(loc = "upper left")
caculate(st_used,st_name)
#calculate_plot()


#create a col
st_used["MACD"] = macd
st_used["signal"] = signal
#buy sell
def buy_sell(name):
    buy = []
    sell = []
    flag = -1
    for i in range(0, len(name)):
        if name["MACD"][i] > name["signal"][i]:
            sell.append(np.nan)
            if flag != 1:
                buy.append(name["Close"][i])
                flag = 1
            else:
                buy.append(np.nan)
        elif name["MACD"][i] < name["signal"][i]:
            buy.append(np.nan)
            if flag != 0:
                sell.append(name["Close"][i])
                flag = 0
            else:
                sell.append(np.nan)
        else:
            buy.append(np.nan)
            sell.append(np.nan)
    return (buy, sell)


#create new col
a = buy_sell(st_used)
st_used["Buy"] = a[0]
st_used["Sell"] = a[1]
#plot
def pol_bs(name):
    plt.figure(figsize=(12.2,4.5))
    plt.scatter(name.index,name["Buy"],label = "Buy", color = "green", marker = "^", alpha = 1)
    plt.scatter(name.index,name["Sell"],label = "Sell", color = "red", marker = "v", alpha = 1)
    name["Close"].plot(label = "Close Price", alpha = 0.35)
    plt.title("Close price : Buy_Sell")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(loc = "upper left")


def sma(data,per = 30 ,col = "Close"):
    return data[col].rolling(window = per).mean()
def rsi(name):
    per = 14
    delta = name["Close"].diff(1)
    delta = delta[1:]
    up = delta.copy()
    down = delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    name["up"] = up
    name ["down"] = down
    avg_gain = sma(name,per, col = "up")
    avg_loss = abs(sma(name, per, col = "down"))
    rs = avg_gain/avg_loss
    rsi = 100.0-(100.0/(1.0+rs))
    name["rsi"] = rsi
    return name
rsi(st_used)
def rsi_plot(name):
    plt.figure(figsize=(12.2,6.4))
    plt.plot(name.index,name["rsi"],label = "rsi", color = "green")
    plt.legend(loc = "upper left")
    plt.title("Close price : RSI")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(loc = "upper left")

#choose
def main(name, select, name_label):
    list = ["Open", "Close", "High", "Low", "Volume"]
    if select in list :
        plt.figure(figsize=(12.2,4.5))
        name[select].plot(label = name_label)
        plt.legend(loc = "upper left")
    elif select == "Macd":
        calculate_plot()
    elif select == "Buy" or select == "Sell":
        pol_bs(st_used)
    elif select == "Rsi":
        rsi_plot(name)

main(st_used, select, st_name)

plt.show()