import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import yfinance as yf


nameI = input().upper()
nameII = input().upper()
nameIII = input().upper()


start_date = input()
end_date = input()

selective = input().capitalize()

class Plotting:
    def __init__(self, sel):
        self.select = sel
    def plo(self, name,started,ended):
        if started == "" and ended == "":
            st_name = yf.download(name)
            st_name[self.select].plot(label = name)
        elif started == "":
            st_name = yf.download(name, start= None, end= ended)
            st_name[self.select].plot(label = name)
        elif ended == "":
            st_name = yf.download(name, start= started, end= None)
            st_name[self.select].plot(label = name)
        else:
            st_name = yf.download(name, start= started, end= ended)
            st_name[self.select].plot(label = name)


def main(i, ii, iii  , start, end, seclect):
    plt.figure(figsize=(50,18))
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.title("priec of"+i+ii+iii)
    p = Plotting(seclect)
    p.plo(i, start, end)
    p.plo(ii, start, end)
    p.plo(iii, start, end)
main(nameI, nameII, nameIII, start_date, end_date, selective)
