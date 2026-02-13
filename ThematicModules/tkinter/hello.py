# -*- coding:utf-8 -*-
# file:hello.py
from tkinter import *

k = Tk()
k.title("")
k.geometry("700x500")

def sc():
    t.delete(0.0, END)

def sz():
    t.config(font="宋体 14 bold italic")

def hy():
    t.delete(0.0, END)
    t.config(font="宋体 10")
    t.insert(1.0, "I love ")
    t.tag_config("tag", background='gold', foreground='green')
    t.insert(END, "python", "tag")

t = Text(k, font="宋体 10")
t.grid(row=0, column=0, rowspan=3)
t.insert(1.0, "I love ")

t.insert(END, "python", "t")
t.tag_config("t", background='gold', foreground='green')

a1 = Button(k, text="文本删除", command=sc)
a1.grid(row=0, column=1)
a2 = Button(k, text="文本设置", command=sz)
a2.grid(row=1, column=1)
a3 = Button(k, text="文本还原", command=hy)
a3.grid(row=2, column=1)

k.mainloop()
