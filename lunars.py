#!/usr/bin/env python3
# coding=utf-8

from tkinter import *
from tkinter.ttk import *
import os
from lunardata import *

__author__ = {'name' : 'TestPoo', 'created' : '2022-05-05', 'modify' : '2023-04-18'}

#**实现界面功能****
class Application_ui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('万年历')
        self.master["bg"]='#f5f5f5'
        self.createWidgets()
        self.position()

    def position(self):
        top.resizable(False,False)
        curWidth = 350
        curHeight = 470
        scnWidth,scnHeight = top.maxsize()
        tmpplace = '%dx%d-%d-%d'%(curWidth,curHeight,2,30)
        top.geometry(tmpplace)
        top.attributes('-type', 'dock')
        top.attributes("-topmost", True)
        top.focus_force()

    def createWidgets(self):
        top = self.winfo_toplevel()

        self.cdate,self.clunar,self.cweek,self.cday = show_month(datetime.now().year, datetime.now().month, datetime.now().day)

        self.style = Style()
        self.style.theme_use('default')
        self.style.configure("Pn.TButton",foreground="#303133",background="#f5f5f5",borderwidth=0,font=('',12),justify='center',relief=FLAT)
        self.style.configure("To.TButton",foreground="#2ca7f8",background="#f5f5f5",borderwidth=0,font=('',12),justify='center',relief=FLAT)
        self.style.configure("Yd.TButton",foreground="#161616",background="#f5f5f5",borderwidth=0,font=('',12),justify='center',relief=FLAT)
        self.style.configure("Ym.TButton",foreground="#161616",background="#f5f5f5",borderwidth=0,font=('',12),anchor='center',relief=FLAT)
        self.style.configure("Wk.TButton",foreground="#363636",background="#f5f5f5",borderwidth=0,font=('',10),anchor='center',relief=FLAT)

        Button(top, text="  "+self.cdate+"\n  "+self.clunar,style="Yd.TButton").place(x=0,y=0,width=350,height=60)
        Separator(top,orient=HORIZONTAL).place(x=0,y=60,width=350,height=2)

        self.preYear = Button(top,text="◀",command = self.pre_year,style="Pn.TButton").place(x=0,y=62,width=30,height=48)
        self.cyear = Button(top, text=self.cdate[0:5],style="Ym.TButton")
        self.cyear.place(x=30,y=62,width=80,height=48)
        self.nextYear = Button(top,text="▶",command = self.next_year,style="Pn.TButton").place(x=110,y=62,width=30,height=48)
        self.preMonth = Button(top,text="◀",command = self.pre_month,style="Pn.TButton").place(x=140,y=62,width=30,height=48)
        self.cmonth = Button(top, text=self.cdate[5:8],style="Ym.TButton")
        self.cmonth.place(x=170,y=62,width=60,height=48)
        self.nextMonth = Button(top,text="▶",command = self.next_month,style="Pn.TButton").place(x=230,y=62,width=30,height=48)
        self.today = Button(top,text="返回今天",command = self.today,style="To.TButton").place(x=260,y=62,width=100,height=48)

        for i in range(len(self.cweek)):
            Button(top,text='周' + self.cweek[i],style="Wk.TButton").place(x=50*i,y=110,width=50,height=50)
        
        self.button_list = []
        self.addButton(self.cday)
        
        top.bind('<FocusOut>', self.lossfocus)
        
    def addButton(self,cday):

        self.style.configure(".TButton",foreground="#fff",background="#2ca7f8",borderwidth=0,font=('',10,'bold'),justify='center',relief=FLAT)
        self.style.configure("*.TButton",foreground="#a8a8a8",background="#f5f5f5",borderwidth=0,font=('',10),justify='center',relief=FLAT)
        self.style.configure("@.TButton",foreground="#e7493e",background="#f5f5f5",borderwidth=0,font=('',10,'bold'),justify='center',relief=FLAT)
        self.style.configure("$.TButton",foreground="#2ca7f8",background="#f5f5f5",borderwidth=0,font=('',10,'bold'),justify='center',relief=FLAT)
        self.style.configure("A.TButton",foreground="#363636",background="#f5f5f5",borderwidth=0,font=('',10),justify='center',relief=FLAT)
        for i in range(len(self.cday)):
            m,n = divmod(i,7)
            if cday[i].split('\n')[0].strip() == str(datetime.now().day):
                self.button = Button(top,text=self.cday[i],style=".TButton")
            elif cday[i][0] == '*':
                self.button = Button(top,text=self.cday[i][1:],command = self.pre_month,style="*.TButton")
            elif cday[i][0] == '#':
                self.button = Button(top,text=self.cday[i][1:],command = self.next_month,style="*.TButton")
            elif cday[i][0] == '@':
                if cday[i][1:].split('\n')[0] == str(datetime.now().day):
                    self.button = Button(top,text=self.cday[i][1:],style="@.TButton")
                else:
                    self.button = Button(top,text=self.cday[i][1:],style="@.TButton")
            elif cday[i][0] == '$':
                if cday[i][1:].split('\n')[0] == str(datetime.now().day):
                    self.button = Button(top,text=self.cday[i][1:],style="$.TButton")
                else:
                    self.button = Button(top,text=self.cday[i][1:],style="$.TButton")
            else:
                self.button = Button(top,text=self.cday[i],style="A.TButton")
            self.button.place(x=50*n,y=160 + 50*m,width=50,height=50)
            self.button_list.append(self.button)

#**实现具体的事件处理回调函数****
class Application(Application_ui):
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    def lossfocus(self, event=None):
        if event.widget == top:
            top.destroy()

    def pre_year(self, event=None):
        for b in self.button_list:
            b.destroy()
        self.year = int(self.cyear.cget("text").replace('年','')) - 1
        self.month = int(self.cmonth.cget("text").replace('月',''))
        self.cyear.config(text=str(self.year)+"年")
        self.cday = show_month(self.year, self.month, 1)[-1]
        self.addButton(self.cday)

    def next_year(self, event=None):
        for b in self.button_list:
            b.destroy()
        self.year = int(self.cyear.cget("text").replace('年','')) + 1
        self.month = int(self.cmonth.cget("text").replace('月',''))
        self.cyear.config(text=str(self.year)+"年")
        self.cday = show_month(self.year, self.month, 1)[-1]
        self.addButton(self.cday)

    def pre_month(self, event=None):
        for b in self.button_list:
            b.destroy()
        self.year = int(self.cyear.cget("text").replace('年',''))
        self.month = int(self.cmonth.cget("text").replace('月','')) - 1
        if self.month == 0:
            self.year = self.year - 1
            self.month = 12
        self.cyear.config(text=str(self.year)+"年")
        self.cmonth.config(text=str(self.month if self.month >= 10 else "0" + str(self.month))+"月")
        self.cday = show_month(self.year, self.month, 1)[-1]
        self.addButton(self.cday)

    def next_month(self, event=None):
        for b in self.button_list:
            b.destroy()
        self.year = int(self.cyear.cget("text").replace('年',''))
        self.month = int(self.cmonth.cget("text").replace('月','')) + 1
        if self.month == 13:
            self.year = self.year + 1
            self.month = 1
        self.cyear.config(text=str(self.year)+"年")
        self.cmonth.config(text=str(self.month if self.month >= 10 else "0" + str(self.month))+"月")
        self.cday = show_month(self.year, self.month, 1)[-1]
        self.addButton(self.cday)

    def today(self, event=None):
        for b in self.button_list:
            b.destroy()
        self.cdates = show_month(datetime.now().year, datetime.now().month, datetime.now().day)
        self.year = int(self.cdates[0][0:4])
        self.month = int(self.cdates[0][5:7])
        self.cyear.config(text=str(self.year)+"年")
        self.cmonth.config(text=str(self.month if self.month >= 10 else "0" + str(self.month))+"月")
        self.cday = show_month(self.year, self.month, 1)[-1]
        self.addButton(self.cday)

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()