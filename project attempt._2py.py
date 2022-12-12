
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
        return  self.df[col].rolling(window = 14).mean()
    def rsi_cal(self, x = "Close"):
        delta = self.df[x].diff(1)
        delta = delta[1:]
        up = delta.copy()
        down = delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        self.df["up"] = up
        self.df["down"] = down
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
        self.df[x].plot(label = x+" Price", alpha = 0.35)
        plt.title(x+ " : Buy_Sell")
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

def defa(x = "Closee"):
    plt.figure(figsize=(12.2,6.4))
    plt.plot(p.df.index,p.df[x])
    plt.legend(loc = "best")
    plt.title(x+"Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

p = Plotting()
def time_check(r):
    dict1={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
    if r=='':
        return True
    try:
        list2=r.split('-')
        if len(list2)!=3:
            return False 
        if  not 1990<=int(list2[0])<=2023:
            return False
        if not 1<=int(list2[1])<=12:
            return False
        if not 1<=int(list2[2])<=dict1[int(list2[1])]:      
            return False
        nnn = datetime.datetime.now()
        nnn = str(nnn).split()
        sss=nnn[0].split('-')
        if int(list2[0])>int(sss[0]):
            return False
        if int(list2[1])>int(sss[1]):
            return False
        if int(list2[2])>int(sss[2]):
            return False    
        return True
    except:
        messagebox.showerror('Error','Invalid input')
        return False            

                        



def main(st,start_date_o,end_date_o,cc,indi):
    a = st.get()
    b = start_date_o.get()
    c = end_date_o.get()
    d = cc.get()
    e = indi.get()
    check_1=time_check(b)
    check_2=time_check(c)
    if check_1 == True and check_2 == True:
        try:
            p.down(a,b,c)
            if len(p.df) == 0:
                messagebox.showerror('Error','Invalid input')    
            elif e == "Default" :
                defa(d)
            elif e == "Short-Long Ema":
                p.short_long_plot(d)
            elif e == "MACD-Signal":
                p.macd_sig_plot(d)
            elif e == "Buy and Sell":
                p.buy_sell_plot(d)
            elif e == "RSI":
                p.rsi_plot(d)
        except:
            messagebox.showerror("remind",'Invalid input')
    else:
        messagebox.showerror('Error_date',"Error Date")        


def gui():
    p = Plotting()

    windows = tk.Tk()
    in_frame = tk.Frame(windows)
    in_frame.pack()

    tk.Label(in_frame,text="Input the Stock's Abbreviation").grid(row=0,column=0)
    st = tk.Entry(in_frame)
    st.grid(row = 0,column=1)
    
    tk.Label(in_frame,text="Start Date [year(XXXX)-month(XX)-days(XX)] : ").grid(row=1,column=0)
    start_date_r = tk.Entry(in_frame)
    start_date_r.grid(row = 1,column=1)

    tk.Label(in_frame,text="End Date [year(XXXX)-month(XX)-days(XX)] : ").grid(row=2,column=0)
    end_date_r = tk.Entry(in_frame)
    end_date_r.grid(row = 2,column= 1)

    tk.Label(in_frame,text = "Chice What type of Graph").grid(row = 3,column= 0)
    cc = tk.StringVar(value="Close")
    choice = ttk.Combobox(in_frame,textvariable= cc)
    choice["values"] = ["Close","Open","High","Low"]
    choice.grid(row = 3,column=1)

    tk.Label(in_frame, text= "What indicator do you want").grid(row = 4,column= 0)
    indi = tk.StringVar(value = "Default")
    choose = ttk.Combobox(in_frame, textvariable= indi)
    choose["value"] = ["Default","Short-Long Ema","MACD-Signal","Buy and Sell","RSI"]
    choose.grid(row = 4, column=1)
    sci=tk.Button(in_frame,text="Send info",command=lambda:main(st,start_date_r,end_date_r,cc,indi),bg="#C19A6B",fg="black")
    sci.grid(row = 6,column=3)


    windows.mainloop()

gui()