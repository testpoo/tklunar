#!/usr/bin/env python3
# coding=utf-8

from tkinter import *
from tkinter.ttk import *
import os
from lunardata import *

__author__ = {'name' : 'TestPoo', 'created' : '2022-05-05', 'modify' : '2022-11-14'}

#**实现界面功能****
class Application_ui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('万年历')
        self.master["bg"]='#fff'
        self.createWidgets()
        self.position()


    def position(self):
        top.resizable(False,False)
        curWidth = 900
        curHeight = 600
        scnWidth,scnHeight = top.maxsize()
        tmpplace = '%dx%d+%d+%d'%(curWidth,curHeight,(scnWidth-curWidth)/2,(scnHeight-curHeight)/2)
        top.geometry(tmpplace)
        top.iconphoto(False, PhotoImage(file=os.getcwd() + '/calendar.png'))

    def createWidgets(self):
        top = self.winfo_toplevel()

        self.cdate,self.clunar,self.cweek,self.cday = show_month(datetime.now().year, datetime.now().month, datetime.now().day)

        self.style = Style()
        self.style.theme_use('default')
        self.style.configure("Pn.TButton",foreground="#303133",background="#fff",borderwidth=0,font=('',12),justify='center',relief=FLAT)
        self.style.configure("To.TButton",foreground="#2ca7f8",background="#fff",borderwidth=0,font=('',12),justify='center',relief=FLAT)
        self.style.configure("Yd.TLabel",foreground="#161616",background="#fff",borderwidth=0,font=('',12,'bold'),anchor='center')
        self.style.configure("Ym.TLabel",foreground="#161616",background="#fff",borderwidth=0,font=('',12),anchor='center')
        self.style.configure("Wk.TLabel",foreground="#363636",background="#eee",borderwidth=0,font=('',10),anchor='center')

        Label(top, text=self.cdate + " "*10 + self.clunar,style="Yd.TLabel").place(x=110,y=0,width=700,height=40)
        Separator(top,orient=HORIZONTAL).place(x=0,y=40,width=900,height=2)

        self.preYear = Button(top,text="◀",command = self.pre_year,style="Pn.TButton").place(x=110,y=42,width=30,height=68)
        self.cyear = Label(top, text=self.cdate[0:5],style="Ym.TLabel")
        self.cyear.place(x=140,y=42,width=80,height=68)
        self.nextYear = Button(top,text="▶",command = self.next_year,style="Pn.TButton").place(x=220,y=42,width=30,height=68)
        self.preMonth = Button(top,text="◀",command = self.pre_month,style="Pn.TButton").place(x=250,y=42,width=30,height=68)
        self.cmonth = Label(top, text=self.cdate[5:8],style="Ym.TLabel")
        self.cmonth.place(x=280,y=42,width=60,height=68)
        self.nextMonth = Button(top,text="▶",command = self.next_month,style="Pn.TButton").place(x=340,y=42,width=30,height=68)
        self.today = Button(top,text="返回今天",command = self.today,style="To.TButton").place(x=690,y=42,width=100,height=68)

        for i in range(len(self.cweek)):
            Label(top,text='周' + self.cweek[i],style="Wk.TLabel").place(x=100 + 100*i,y=110,width=100,height=50)
        
        self.button_list = []
        self.addButton(self.cday)
        
    def addButton(self,cday):

        self.style.configure(".TButton",foreground="#fff",background="#2ca7f8",borderwidth=0,font=('',10,'bold'),justify='center',relief=FLAT)
        self.style.configure("*.TButton",foreground="#a8a8a8",background="#fff",borderwidth=0,font=('',10),justify='center',relief=FLAT)
        self.style.configure("@.TButton",foreground="#e7493e",background="#fff",borderwidth=0,font=('',10,'bold'),justify='center',relief=FLAT)
        self.style.configure("$.TButton",foreground="#2ca7f8",background="#fff",borderwidth=0,font=('',10,'bold'),justify='center',relief=FLAT)
        self.style.configure("A.TButton",foreground="#363636",background="#fff",borderwidth=0,font=('',10),justify='center',relief=FLAT)
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
            self.button.place(x=100 + 100*n,y=160+70*m,width=100,height=70)
            self.button_list.append(self.button)

#**实现具体的事件处理回调函数****
class Application(Application_ui):
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

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