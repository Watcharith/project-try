
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import tkinter as tk

class Calculate:

    def __init__(self, name):
        self.name = name
        self.df = ""
    def down(self, start_date = "", end_date = ""):
        if start_date == "" and end_date == "":
            self.df = yf.download(self.name)
        elif start_date == "":
            self.df = yf.download(self.name, end= end_date)
        elif end_date == "" :
            self.df = yf.download(self.name, start= start_date)
        else:
            self.df = yf.download(self.name, start= start_date, end= end_date)
    def short_long(self, x = "Close"):
        self.short = self.df[x].ewm(span = 12, adjust = False).mean()
        self.long = self.df[x].ewm(span = 26, adjust = False).mean()


class Plotting(Calculate):

    def __init__(self, name, start_date = "", end_date = ""):
        super().__init__(name)
        super().down(start_date,end_date)
    def pp():
        print(p)

p = Plotting("TCS")
p.short_long()
print(p.short)