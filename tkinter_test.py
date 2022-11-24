import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import yfinance as yf
import tkinter as tk

tkin = tk.Tk()
tkin.title("Stock Graph")
window = tk.Frame(tkin, background="light pink")
tk.Grid()

name_abb = tk.Label(tkin, text = "Stock's Abbreviation").grid(row = 0,column = 4)
name = tk.Entry(tkin, bg ="#C19A6B", fg="black").grid(row = 0, column = 5)

start_date =  tk.Label(tkin, text = "Start Date : ").grid(row = 1,column = 4)
start_date_in = tk.Entry(tkin, bg ="#C19A6B", fg="black").grid(row = 1, column = 5)

end_date = tk.Label(tkin, text = "End Date : ").grid(row = 2,column = 4)
end_date_in = tk.Entry(tkin, bg ="#C19A6B", fg="black").grid(row = 2, column = 5)

select = tk.Label(tkin, text = "choose what you want : ").grid(row = 3,column = 3)

open_t = tk.Checkbutton(tkin, onvalue = "Open", offvalue = None).grid(row = 4, column = 3)
open_l =  tk.Label(tkin, text = "Open").grid(row = 4,column = 4)
close_t = open_t = tk.Checkbutton(tkin, onvalue = "Close", offvalue = None).grid(row = 4, column = 5)
close_l =  tk.Label(tkin, text = "Close").grid(row = 4,column = 6)
high_t = tk.Checkbutton(tkin, onvalue = "High", offvalue = None).grid(row = 5, column = 3)
high_l =  tk.Label(tkin, text = "High").grid(row = 5,column = 4)
low_t = open_t = tk.Checkbutton(tkin, onvalue = "Low", offvalue = None).grid(row = 5, column = 5)
low_l =  tk.Label(tkin, text = "Low").grid(row = 5,column = 6)

ma_sin = tk.Checkbutton(tkin, onvalue = "MACD", offvalue = None).grid(row = 6, column = 3)
open_l =  tk.Label(tkin, text = "MACD/Signal").grid(row = 6,column = 4)
rsi_t = tk.Checkbutton(tkin, onvalue = "Rsi", offvalue = None).grid(row = 6, column = 5)
rsi_l =  tk.Label(tkin, text = "RSI").grid(row = 6,column = 6)

buy_t = tk.Checkbutton(tkin, onvalue = "Buy", offvalue = None).grid(row = 4, column = 3)
buy_l =  tk.Label(tkin, text = "Buy").grid(row = 4,column = 4)
sell_t = open_t = tk.Checkbutton(tkin, onvalue = "Sell", offvalue = None).grid(row = 4, column = 5)
sell_l =  tk.Label(tkin, text = "Sell").grid(row = 4,column = 6)

def sma(data,per = 30 ,col = "Close"):
    return data[col].rolling(window = per).mean()

class caluclate:

    def __init__(self, name):
        self.name = name

    def down(self):
        global started,ended
        if started == "" and ended == "":
            self.st_use = yf.download(self.name)
        elif started == "":
            self.st_use = yf.download(self.name, start = None ,end= ended)
        elif ended == "":
            self.st_use = yf.download(self.name, start= started, end = None)
        else:
            self.st_use = yf.download(self.name, start= started, end=ended)

    def calculate(self):
        short = self.st_use.Close.ewm(span = 12, adjust = False).mean()
        long = self.st_use.Close.ewm(span = 26, adjust = False).mean()
        self.macd = short - long
        self.signal = self.macd.ewm(span = 9, adjust = False).mean()
        self.st_use["MACD"] = self.macd
        self.st_use["signal"] = self.signal

    def buy_sell(self):
        buy = []
        sell = []
        flag = -1
        for i in range(0, len(self.st_use)):
            if self.st_use["MACD"][i] > self.st_use["signal"][i]:
                sell.append(np.nan)
                if flag != 1:
                    buy.append(self.st_use["Close"][i])
                    flag = 1
                else:
                    buy.append(np.nan)
            elif self.st_use["MACD"][i] < self.st_use["signal"][i]:
                buy.append(np.nan)
                if flag != 0:
                    sell.append(self.st_use["Close"][i])
                    flag = 0
                else:
                    sell.append(np.nan)
            else:
                buy.append(np.nan)
                sell.append(np.nan)
        self.st_use["Sell"] = sell #has been change
        self.st_use["Buy"] = buy

    def rsi(self):
        per = 14
        delta = self.st_use["Close"].diff(1)
        delta = delta[1:]
        up = delta.copy()
        down = delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        self.st_use["up"] = up
        self.st_use ["down"] = down
        avg_gain = sma(self.st_use,per, col = "up")
        avg_loss = abs(sma(self.st_use,per, col = "down"))
        rs = avg_gain/avg_loss
        rsi = 100.0-(100.0/(1.0+rs))
        self.st_use["rsi"] = rsi


class Plotting(caluclate):
    def __init__(self, name):
        super().__init__(name)
        super().down()

    def calculate_plot(self):
        plt.figure(figsize=(12.2,4.5))
        self.macd.plot(label = "MACD", color = "green")
        self.signal.plot(label = "Signal", color = "black")
        plt.legend(loc = "upper left")
        plt.show()

    def buy_plot(self):
        plt.figure(figsize=(12.2,4.5))
        plt.scatter(self.st_use.index,self.st_use["Buy"],label = "Buy", color = "green", marker = "^", alpha = 1)
        self.st_use["Close"].plot(label = "Close Price", alpha = 0.35)
        plt.title("Close price : Buy_Sell")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend(loc = "upper left")
        #plt.show()
    def sell_plot(self):
        plt.figure(figsize=(12.2,4.5))
        plt.scatter(self.st_use.index,self.st_use["Sell"],label = "Sell", color = "red", marker = "v", alpha = 1)
        self.st_use["Close"].plot(label = "Close Price", alpha = 0.35)
        plt.title("Close price : Buy_Sell")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend(loc = "upper left")
    def rsi_plot(self):
        plt.figure(figsize=(12.2,6.4))
        plt.plot(self.st_use.index,self.st_use["rsi"],label = "rsi", color = "green")
        plt.legend(loc = "upper left")
        plt.title("Close price : RSI")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend(loc = "upper left")


tkin.mainloop()