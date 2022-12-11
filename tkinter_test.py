import tkinter as tk

root = tk.Tk()
root.title("My GUI")
tk.Label (text = "Hello world").place(x=0,y=0)
#size
root.geometry("500x400+100+0")
root.mainloop()