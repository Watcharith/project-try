

import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import tkinter as tk
from tkinter import messagebox

class Process:
    def __init__(self):
        self.start = dt.datetime(2018,1,1)
        self.end = dt.datetime.now()
        self.tickers = []
        self.colnames = []
        self.combined = ""
    def work(self,x,operation):
        use = x.get()
        if use == "":
            messagebox.showerror("INPUT","No Input")
        else:
            if operation == "ADD":
                if use.capitalize() in self.tickers:
                    messagebox.showerror("Have it","This name already in list")
                else:
                    self.tickers.append(use.capitalize())
            elif operation == "Remove":
                if use.capitalize() not in self.tickers:
                    messagebox.showerror("No name","No name in that list")
                else:
                    self.tickers.remove(use.capitalize())

        
    def show(self):
        if len(self.tickers) == 0:
            messagebox.showerror("No input","Nothing in the program")
        else:
            self.combined = ""
            self.colnames = []
            for ticker in self.tickers:
                data = web.DataReader(ticker, "yahoo",self.start, self.end)
                if len(self.colnames) == 0:
                    self.combined = data[['Adj Close']].copy()
                else:
                    self.combined = self.combined.join(data['Adj Close'])
                self.colnames.append(ticker)
                self.combined.columns = self.colnames

            corr_data = self.combined.pct_change().corr(method="pearson")
            sns.heatmap(corr_data, annot=True, cmap="coolwarm")

            plt.show()

class Gui(Process):
    def __init__(self):
        super().__init__()
        self.tkin = tk.Tk()
        self.canva = tk.Frame(self.tkin)
        self.canva.pack()
    def front(self):

        tk.Label(self.canva,text = "ADD ticker").grid(row = 0,column=0)
        tic = tk.StringVar()
        tic_en = tk.Entry(self.canva,textvariable=tic)
        tic_en.grid(row = 0,column=1)

        a = tk.Button(self.canva,text = "ADD",command = lambda: self.work(tic,"ADD"),bg = "cyan")
        a.grid(row = 1,column=0)

        b = tk.Button(self.canva,text = "Remove",command = lambda: self.work(tic,"Remove"),bg = "red")
        b.grid(row = 1,column=1)

        c = tk.Button(self.canva,text = "Plot",command = lambda: self.show(),bg = "grey")
        c.grid(row = 1,column=2)
        self.tkin.mainloop()
gui = Gui()
gui.front()