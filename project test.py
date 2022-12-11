
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import tkinter as tk
from tkinter import ttk,messagebox

plt.style.use("fivethirtyeight")

class Calculate:

    def __init__(self):
        self.df = ""
    def down(self, name,start_date = "", end_date = ""):
        if start_date == "" and end_date == "":
            self.df = yf.download(name)
        elif start_date == "":
            self.df = yf.download(name, end= end_date)
        elif end_date == "" :
            self.df = yf.download(name, start= start_date)
        else:
            self.df = yf.download(name, start= start_date, end= end_date)
    def short_long(self, x = "Close"):
        self.x = x
        self.short = self.df[x].ewm(span = 12, adjust = False).mean()
        self.long = self.df[x].ewm(span = 26, adjust = False).mean()
        self.df["Short"] = self.short
        self.df["Long"] = self.long
    def macd_sig(self, x = "Close"):
        self.short_long(x)
        self.macd = self.short - self.long
        self.signal = self.macd.ewm(span = 9, adjust = False).mean()
        self.df["MACD"] = self.macd
        self.df["signal"] = self.signal
    def buy_sell(self, x = "Close"):

        self.macd_sig(x)

        buy = []
        sell = []
        flag = -1
        for i in range(0, len(self.df)):
            if self.df["MACD"][i] > self.df["signal"][i]:
                sell.append(np.nan)
                if flag != 1:
                    buy.append(self.df["Close"][i])
                    flag = 1
                else:
                    buy.append(np.nan)
            elif self.df["MACD"][i] < self.df["signal"][i]:
                buy.append(np.nan)
                if flag != 0:
                    sell.append(self.df["Close"][i])
                    flag = 0
                else:
                    sell.append(np.nan)
            else:
                buy.append(np.nan)
                sell.append(np.nan)
        self.df["Sell"] = buy #has been change
        self.df["Buy"] = sell
    def sma_cal(self ,col = "Close"):
        return self.df[col].rolling(window = 14).mean()
    def rsi_cal(self, x = "Close"):
        delta = self.df[x].diff(1)
        delta = delta[1:]
        up = delta.copy()
        down = delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        self.df["up"] = up
        self.df ["down"] = down
        avg_gain = self.sma_cal(col = "up")
        avg_loss = abs(self.sma_cal(col = "down"))
        rs = avg_gain/avg_loss
        rsi = 100.0-(100.0/(1.0+rs))
        self.df["rsi"] = rsi


class Plotting(Calculate):

    def __init__(self):
        super().__init__()
    def short_long_plot(self, x = "Close"):
        super().short_long(x)
        plt.figure(figsize= (12.2,6.4))
        self.short.plot(label = "Short", color = "green")
        self.long.plot(label = "Long", color = "red")
        plt.legend(loc = "best")
        plt.title("Short and long")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.show()
    def macd_sig_plot(self, x = "Close"):
        super().macd_sig(x)
        plt.figure(figsize= (12.2,6.4))
        self.macd.plot(label = "macd", color = "green")
        self.signal.plot(label = "signal", color = "red")
        plt.legend(loc = "best")
        plt.title("macd and signal")
        plt.xlabel("Date")
        plt.ylabel("Scale")
        plt.show()
    def buy_sell_plot(self, x = "Close" ):
        super().buy_sell(x)
        plt.figure(figsize=(12.2,4.5))
        plt.scatter(self.df.index,self.df["Buy"],label = "Buy", color = "green", marker = "^", alpha = 1)
        plt.scatter(self.df.index,self.df["Sell"],label = "Sell", color = "red", marker = "v", alpha = 1)
        self.df[self.x].plot(label = self.x+" Price", alpha = 0.35)
        plt.title(self.x+ " : Buy_Sell")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend(loc = "best")
        plt.show()
    def rsi_plot(self, x ="Close"):
        super().rsi_cal(x)
        plt.figure(figsize=(12.2,6.4))
        plt.plot(self.df.index,self.df["rsi"],label = "rsi", color = "green")
        plt.title( x+" : RSI")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend(loc = "best")
        plt.show()

p = Plotting()
p.down("aapl")
p.rsi_cal()
p.rsi_plot()