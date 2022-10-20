#!/usr/bin/env python3
# coding=utf-8

from tkinter import *
from tkinter import ttk
import os
import sys
from lunardata import *
from config import *

__author__ = {'name' : 'TestPoo', 'created' : '2022-05-05', 'modify' : '2022-10-19'}

#**实现界面功能****
class Application_ui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.dpi=self.xdpi()
        self.master.title('万年历')
        self.master["bg"]='#fff'
        self.createWidgets()
        self.position()

    def xdpi(self):
        self.xdpi = 1
        temps = os.popen('xrdb -query').readlines()
        if temps != '':
            for temp in temps:
                temp = temp.split(':')
                if temp[0] == 'Xft.dpi':
                    self.xdpi = int(temp[1].replace('\n','').replace('\t',''))/96
                break
        return self.xdpi

    def position(self):
        top.attributes('-type', 'dock')
        top.resizable(False,False)
        curWidth = top.winfo_width() # 获取窗口宽度
        curHeight = top.winfo_height() # 获取窗口高度
        tmpplace = '%dx%d%s%s'%(curWidth,curHeight,config['lright'],config['tbottom'])
        top.geometry(tmpplace)
        top.geometry('%dx%d'%(315*self.dpi,455*self.dpi))
        top.attributes("-topmost", True)   # 最上层显示
        top.focus_force()   # 获取焦点

    def createWidgets(self):
        top = self.winfo_toplevel()

        self.nyr,self.nlnyr,self.xinqi,self.rilitian = show_month(datetime.now().year, datetime.now().month, datetime.now().day)
        
        self.style = ttk.Style()
        self.style.configure("TLabel",foreground="#000",background="#fff",font=('',config['fontSize']+2))
        self.style.configure("Title.TLabel",foreground="#2e4e7e",font=('',config['fontSize']+2,"bold"))
        self.style.configure("TButton",foreground="#000",background="#fff",borderwidth=0,font=('',config['fontSize']),justify='center',relief=FLAT)
        self.style.configure("Today.TButton",background="#ccc")
        self.style.configure("PerNext.TButton",foreground="#aaa")
        self.style.configure("Festival.TButton",foreground="#845a33")
        self.style.configure("Solarterms.TButton",foreground="#2e4e7e")
        self.style.configure("FestivalT.TButton",foreground="#845a33",background="#ccc")
        self.style.configure("SolartermsT.TButton",foreground="#2e4e7e",background="#ccc")
        self.style.configure("Set.TButton",foreground="#2e4e7e",justify='left')
        
        ttk.Label(top, text=self.nyr,anchor='w',style="Title.TLabel").place(x=10*self.dpi,y=0,width=305*self.dpi,height=22*self.dpi)
        ttk.Label(top, text=self.nlnyr,anchor='w',style="Title.TLabel").place(x=10*self.dpi,y=22*self.dpi,width=305*self.dpi,height=23*self.dpi)
        self.label1 = ttk.Label(top, text=self.nyr[0:7],anchor='w')
        self.label1.place(x=10,y=65*self.dpi,width=245*self.dpi,height=45*self.dpi)
        
        for i in range(len(self.xinqi)):
            ttk.Label(top,text=self.xinqi[i],anchor='center').place(x=45*self.dpi*i,y=110*self.dpi,width=45*self.dpi,height=30*self.dpi)
        
        self.button_list = []
        self.addButton(self.rilitian)
        
    def addButton(self,rilitian):
        for i in range(len(self.rilitian)):
            m,n = divmod(i,7)
            if rilitian[i].split('\n')[0].strip() == str(datetime.now().day):
                self.button = ttk.Button(top,text=self.rilitian[i],style="Today.TButton")
            elif rilitian[i][0] == '*':
                self.button = ttk.Button(top,text=self.rilitian[i][1:],command = self.pre_Cal,style="PerNext.TButton")
            elif rilitian[i][0] == '#':
                self.button = ttk.Button(top,text=self.rilitian[i][1:],command = self.next_Cal,style="PerNext.TButton")
            elif rilitian[i][0] == '@':
                if rilitian[i][1:].split('\n')[0] == str(datetime.now().day):
                    self.button = ttk.Button(top,text=self.rilitian[i][1:],style="FestivalT.TButton")
                else:
                    self.button = ttk.Button(top,text=self.rilitian[i][1:],style="Festival.TButton")
            elif rilitian[i][0] == '$':
                if rilitian[i][1:].split('\n')[0] == str(datetime.now().day):
                    self.button = ttk.Button(top,text=self.rilitian[i][1:],style="SolartermsT.TButton")
                else:
                    self.button = ttk.Button(top,text=self.rilitian[i][1:],style="Solarterms.TButton")
            else:
                self.button = ttk.Button(top,text=self.rilitian[i])
            self.button.place(x=45*self.dpi*n,y=140*self.dpi+45*self.dpi*m,width=45*self.dpi,height=45*self.dpi)
            self.button_list.append(self.button)
        
        ttk.Button(top,text="◀",command = self.pre_Cal).place(x=255*self.dpi,y=65*self.dpi,width=30*self.dpi,height=45*self.dpi)
        ttk.Button(top,text="▶",command = self.next_Cal).place(x=285*self.dpi,y=65*self.dpi,width=30*self.dpi,height=45*self.dpi)
        ttk.Separator(top,orient=HORIZONTAL).place(x=0,y=54*self.dpi,width=315*self.dpi,height=2*self.dpi)
        ttk.Button(top,text="位置和字号设置",command = self.setCal,style="Set.TButton").place(x=0,y=410*self.dpi,width=315*self.dpi,height=45*self.dpi)
    
        ttk.Label(top, text="左右",anchor='center').place(x=10*self.dpi,y=465*self.dpi,width=45*self.dpi,height=30*self.dpi)
        self.firstEntry = StringVar(value=config['lright'])
        self.lright = ttk.Entry(top,justify='center',textvariable=self.firstEntry).place(x=60*self.dpi,y=465*self.dpi,width=45*self.dpi,height=30*self.dpi)
        ttk.Label(top, text="上下",anchor='center').place(x=110*self.dpi,y=465*self.dpi,width=45*self.dpi,height=30*self.dpi)
        self.secondEntry = StringVar(value=config['tbottom'])
        self.tbottom = ttk.Entry(top,justify='center',textvariable=self.secondEntry).place(x=160*self.dpi,y=465*self.dpi,width=45*self.dpi,height=30*self.dpi)
        ttk.Label(top, text="字号",anchor='center').place(x=210*self.dpi,y=465*self.dpi,width=45*self.dpi,height=30*self.dpi)
        self.thirdEntry = StringVar(value=config['fontSize'])
        self.fontSize = ttk.Entry(top,justify='center',textvariable=self.thirdEntry).place(x=260*self.dpi,y=465*self.dpi,width=45*self.dpi,height=30*self.dpi)
    
        ttk.Button(top,text="保存",command = self.setSave,style="Set.TButton").place(x=0*self.dpi,y=500*self.dpi,width=315*self.dpi,height=40*self.dpi)
        
        top.bind('<FocusOut>', self.lossfocus)   # 失去焦点时，关闭窗口

#**实现具体的事件处理回调函数****
class Application(Application_ui):
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    def lossfocus(self, event=None):
        if event.widget == top:
            top.destroy()

    def pre_Cal(self, event=None):
        for b in self.button_list:
            b.destroy()
        self.ym = self.label1.cget("text")
        self.year = int(self.ym[0:4])
        self.month = int(self.ym[5:7].replace('月','')) - 1
        if self.month == 0:
            self.year = self.year - 1
            self.month = 12
        self.label1.config(text=str(self.year)+"年"+str(self.month)+"月")
        self.rilitian = show_month(self.year, self.month, 1)[-1]
        self.addButton(self.rilitian)

    def next_Cal(self, event=None):
        for b in self.button_list:
            b.destroy()
        self.ym = self.label1.cget("text")
        self.year = int(self.ym[0:4])
        self.month = int(self.ym[5:7].replace('月','')) + 1
        if self.month == 13:
            self.year = self.year + 1
            self.month = 1
        self.label1.config(text=str(self.year)+"年"+str(self.month)+"月")
        self.rilitian = show_month(self.year, self.month, 1)[-1]
        self.addButton(self.rilitian)
    
    def setSave(self, event=None):
        value1 = self.firstEntry.get()
        value2 = self.secondEntry.get()
        value3 = int(self.thirdEntry.get())
        tempConfig = "# coding=utf-8\n\nconfig = {'lright':'%s','tbottom':'%s','fontSize':%d}"%(value1,value2,value3)
        # 
        if os.path.exists(os.getcwd()+'/.xfce-lunar/config.py'):
            path = os.getcwd()+'/.xfce-lunar'
        else:
            path = os.getcwd()
        with open('/home/poo/log','w') as t:
            t.write(path+'/config.py')
        with open(path+'/config.py','w',encoding='utf-8') as f:
            f.write(tempConfig)
        python = sys.executable
        os.execl(python, python, * sys.argv)
    
    def setCal(self, event=None):
        top.geometry('%dx%d'%(315*self.dpi,540*self.dpi))

if __name__ == "__main__":
    top = Tk()
    #top.resizable(width=False, height=False)
    Application(top).mainloop()
