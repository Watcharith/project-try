import tkinter as tk

window = tk.Tk()

in_frame = tk.Frame(window)
in_frame.pack()

def destroy():
    for widgets in in_frame.winfo_children():
        widgets.destroy()
def create():
    global x
    x = tk.Entry(in_frame)
    x.grid(row=1,column=1)
def ppp():
    y = int(x.get())
    print(type(y))
def showup():
    destroy()
    tk.Label(in_frame,text="Input the file name (in form name.txt):").grid(row=1,column=0)
    create()
    z = tk.Button(in_frame, command = ppp, text ="Click").grid(row=1, column = 1 )
a = tk.Button(in_frame,command=showup,text="COLLECT DATA").grid(row=0,column=0)
tk.Label(in_frame,text="    ").grid(row=0,column=1)
b = tk.Button(in_frame,command=showup,text="RETRIEVE DATA").grid(row=0,column=2)

window.mainloop()
