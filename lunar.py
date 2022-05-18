#!/usr/bin/env python3
# coding=utf-8

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
from lunardata import *
from config import *
from pathlib import Path

__author__ = {'name' : 'TestPoo', 'created' : '2022-05-05'}

#**实现界面功能****
class Application_ui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.dpi=self.xdpi()
        self.master.title('万年历')
        self.master["bg"]='#fff'
        self.master.geometry('%dx%d'%(315*self.dpi,455*self.dpi))
        self.createWidgets()
        self.position()

    def xdpi(self):
        temps = os.popen('xrdb -query').readlines()

        for temp in temps:
            temp = temp.split(':')
            if temp[0] == 'Xft.dpi':
                self.xdpi = int(temp[1].replace('\n','').replace('\t',''))/96
            else:
                self.xdpi = 1
        return self.xdpi

    def position(self):
        #top.overrideredirect(True)
        top.attributes('-type', 'dock')
        top.resizable(False,False)
        top.iconify() # 隐藏窗口
        top.update() # 更新窗口
        curWidth = top.winfo_width() # 获取窗口宽度
        curHeight = top.winfo_height() # 获取窗口高度
        #scnWidth,scnHeight = top.maxsize() # 获取屏幕宽度和高度
        if config['place'] == '左上':
            tmpplace = '%dx%d+%d+%d'%(curWidth,curHeight,config['left'],config['top'])
        elif config['place'] == '右下':
            tmpplace = '%dx%d-%d-%d'%(curWidth,curHeight,config['right'],config['bottom'])
        elif config['place'] == '右上':
            tmpplace = '%dx%d-%d+%d'%(curWidth,curHeight,config['right'],config['top'])
        elif config['place'] == '左下':
            tmpplace = '%dx%d+%d-%d'%(curWidth,curHeight,config['left'],config['bottom'])
        top.geometry(tmpplace)
        top.deiconify()   # 显示窗口
        top.attributes("-topmost", True)   # 最上层显示
        #top.after(1, lambda: top.focus_force())
        top.focus_force()   # 获取焦点

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.nyr,self.nlnyr,self.xinqi,self.rilitian = show_month(datetime.now().year, datetime.now().month, datetime.now().day)
        
        self.style = ttk.Style()
        self.style.configure("TLabel",foreground="#000",background="#fff",font=(config['font'],config['fontSize']))
        self.style.configure("Title.TLabel",foreground="#2e4e7e",font=(config['font'],config['fontSize'],"bold"))
        self.style.configure("TButton",foreground="#000",background="#fff",borderwidth=0,font=(config['font'],config['fontSize']),justify='center',relief=FLAT)
        self.style.configure("Today.TButton",background="#ccc")
        self.style.configure("PerNext.TButton",foreground="#aaa")
        self.style.configure("Festival.TButton",foreground="#845a33")
        self.style.configure("Solarterms.TButton",foreground="#2e4e7e")
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
                self.button = ttk.Button(top,text=self.rilitian[i][1:],style="Festival.TButton")
            elif rilitian[i][0] == '$':
                self.button = ttk.Button(top,text=self.rilitian[i][1:],style="Solarterms.TButton")
            else:
                self.button = ttk.Button(top,text=self.rilitian[i])
            self.button.place(x=45*self.dpi*n,y=140*self.dpi+45*self.dpi*m,width=45*self.dpi,height=45*self.dpi)
            self.button_list.append(self.button)
        
        ttk.Button(top,text="⮜",command = self.pre_Cal).place(x=255*self.dpi,y=65*self.dpi,width=30*self.dpi,height=45*self.dpi)
        ttk.Button(top,text="➤",command = self.next_Cal).place(x=285*self.dpi,y=65*self.dpi,width=30*self.dpi,height=45*self.dpi)
        ttk.Separator(top,orient=HORIZONTAL).place(x=0,y=54*self.dpi,width=315*self.dpi,height=2*self.dpi)
        ttk.Button(top,text="位置和字体设置",command = self.setCal,style="Set.TButton").place(x=0,y=410*self.dpi,width=315*self.dpi,height=45*self.dpi)
        
        top.bind('<FocusOut>', self.lossfocus)   # 失去焦点时，关闭窗口

#**实现具体的事件处理回调函数****
class Application(Application_ui):
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
        # 直接执行和加入一般监视器路径兼容
        self.filePath = Path(os.getcwd() + "/.xfce-lunar/clock.png")
        if self.filePath.is_file():
            self.file = os.getcwd() + "/.xfce-lunar/"
        else:
            self.file = os.getcwd() + "/"

    def lossfocus(self, event=None):
        if event.widget == top:
            self.top.destroy()

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

    def go(self, event=None):
        if self.placeComvalue.get() == '左上':
            self.varlabel1.set('左')
            self.varlabel2.set('上')
            self.firstEntry.set(config['left'])
            self.secondEntry.set(config['top'])
        elif self.placeComvalue.get() == '右上':
            self.varlabel1.set('右')
            self.varlabel2.set('上')
            self.firstEntry.set(config['right'])
            self.secondEntry.set(config['top'])
        elif self.placeComvalue.get() == '左下':
            self.varlabel1.set('左')
            self.varlabel2.set('下')
            self.firstEntry.set(config['left'])
            self.secondEntry.set(config['bottom'])
        elif self.placeComvalue.get() == '右下':
            self.varlabel1.set('右')
            self.varlabel2.set('下')
            self.firstEntry.set(config['right'])
            self.secondEntry.set(config['bottom'])
    
    def setSave(self, event=None):
        if self.placeComvalue.get() == '左上':
            value1 = int(self.firstEntry.get())
            value2 = int(self.secondEntry.get())
            value3 = self.fontComvalue.get()
            value4 = int(self.fontSizeEntry.get())
            tempConfig = "# coding=utf-8\n\nconfig = {'place':'%s','left':%d,'right':%d,'top':%d,'bottom':%d,'font':'%s','fontSize':%d}"%('左上',value1,0,value2,0,value3,value4)
        elif self.placeComvalue.get() == '右上':
            value1 = int(self.firstEntry.get())
            value2 = int(self.secondEntry.get())
            value3 = self.fontComvalue.get()
            value4 = int(self.fontSizeEntry.get())
            tempConfig = "# coding=utf-8\n\nconfig = {'place':'%s','left':%d,'right':%d,'top':%d,'bottom':%d,'font':'%s','fontSize':%d}"%('右上',0,value1,value2,0,value3,value4)
        elif self.placeComvalue.get() == '左下':
            value1 = int(self.firstEntry.get())
            value2 = int(self.secondEntry.get())
            value3 = self.fontComvalue.get()
            value4 = int(self.fontSizeEntry.get())
            tempConfig = "# coding=utf-8\n\nconfig = {'place':'%s','left':%d,'right':%d,'top':%d,'bottom':%d,'font':'%s','fontSize':%d}"%('左下',value1,0,0,value2,value3,value4)
        elif self.placeComvalue.get() == '右下':
            value1 = int(self.firstEntry.get())
            value2 = int(self.secondEntry.get())
            value3 = self.fontComvalue.get()
            value4 = int(self.fontSizeEntry.get())
            tempConfig = "# coding=utf-8\n\nconfig = {'place':'%s','left':%d,'right':%d,'top':%d,'bottom':%d,'font':'%s','fontSize':%d}"%('右下',0,value1,0,value2,value3,value4)
        with open(self.file + 'config.py','w',encoding='utf-8') as f:
            f.write(tempConfig)
        messagebox.showinfo('提示','修改成功~！')

    def setCal(self, event=None):
        self.top.destroy()
        set = Tk()
        set.title("万年历设置")
        set.resizable(0,0)
        set['background'] = '#f6f5f4'
        set.geometry("%dx%d"%(290*self.dpi,170*self.dpi))
        set.attributes("-topmost", True)
        set.iconphoto(False, PhotoImage(file=self.file + 'clock.png'))
    
        self.setStyle = ttk.Style()
        self.setStyle.configure("TLabel",foreground="#000",background="#f6f5f4",borderwidth=0,font=(config['font'],config['fontSize']))
        self.setStyle.configure("TFrame",foreground="#000",background="#f6f5f4",borderwidth=0,font=(config['font'],config['fontSize']))
        self.setStyle.configure("TButton",foreground="#000",background="#ddd",borderwidth=0,activebackground="#fff",highlightbackground="#fff",font=(config['font'],config['fontSize']),relief=FLAT)
        self.setStyle.configure('TEntry',borderwidth=0)
        self.setStyle.configure('TCombobox',borderwidth=0,background="#d9d9d9",relief=FLAT)
        self.setStyle.configure("TScrollbar",borderwidth=-3)
    
        ttk.Label(set, text="位置",anchor='center').place(x=10*self.dpi,y=10*self.dpi,width=45*self.dpi,height=30*self.dpi)
        self.placeComvalue=StringVar(value=config['place'])#窗体自带的文本，新建一个值
        self.placeComboxlist=ttk.Combobox(set,textvariable=self.placeComvalue,justify='center',state='readonly',font=(config['font'],config['fontSize'])) #初始化
        self.placeComboxlist["values"]=("左上","左下","右上","右下")
        #self.placeComboxlist.current(0) #选择第一个
        self.placeComboxlist.bind("<<ComboboxSelected>>",self.go) #绑定事件,(下拉列表框被选中时，绑定go()函数)
        self.placeComboxlist.place(x=60*self.dpi,y=10*self.dpi,width=220*self.dpi,height=30*self.dpi)
        self.varlabel1 = StringVar(value=config['place'][0])
        ttk.Label(set,textvariable=self.varlabel1,anchor='center').place(x=10*self.dpi,y=50*self.dpi,width=45*self.dpi,height=30*self.dpi)
        if self.placeComvalue.get()[0] == '左':
            self.firstEntry = StringVar(value=config['left'])
        elif self.placeComvalue.get()[0] == '右':
            self.firstEntry = StringVar(value=config['right'])
        self.first = ttk.Entry(set,justify='center',textvariable=self.firstEntry).place(x=60*self.dpi,y=50*self.dpi,width=80*self.dpi,height=30*self.dpi)
        self.varlabel2 = StringVar(value=config['place'][1])
        ttk.Label(set,textvariable=self.varlabel2,anchor='center').place(x=150*self.dpi,y=50*self.dpi,width=45*self.dpi,height=30*self.dpi)
        if self.placeComvalue.get()[1] == '上':
            self.secondEntry = StringVar(value=config['top'])
        elif self.placeComvalue.get()[1] == '下':
            self.secondEntry = StringVar(value=config['bottom'])
        self.second = ttk.Entry(set,justify='center',textvariable=self.secondEntry,font=(config['font'],config['fontSize'])).place(x=200*self.dpi,y=50*self.dpi,width=80*self.dpi,height=30*self.dpi)
    
        temp = os.popen('fc-list :lang=Zh')
        fonts = []
        for line in temp.readlines():
            line = line.split(':')[1].split(',')[0].strip()
            if line not in fonts:
                fonts.append(line)
    
        ttk.Label(set, text="字体",anchor='center').place(x=10*self.dpi,y=90*self.dpi,width=45*self.dpi,height=30*self.dpi)
        self.fontComvalue=StringVar(value=config['font'])
        self.fontComboxlist=ttk.Combobox(set,justify='center',textvariable=self.fontComvalue,state='readonly',font=(config['font'],config['fontSize']))
        self.fontComboxlist["values"]=fonts
        #self.fontComboxlist.current(0)
        self.fontComboxlist.place(x=60*self.dpi,y=90*self.dpi,width=190*self.dpi,height=30*self.dpi)
        self.fontSizeEntry = StringVar(value=config['fontSize'])
        self.fontSize = ttk.Entry(set,justify='center',textvariable=self.fontSizeEntry,font=(config['font'],config['fontSize'])).place(x=252*self.dpi,y=90*self.dpi,width=28*self.dpi,height=30*self.dpi)
        ttk.Button(set,text="保存",command = self.setSave).place(x=10*self.dpi,y=130*self.dpi,width=270*self.dpi,height=30*self.dpi)
        set.mainloop()

if __name__ == "__main__":
    top = Tk()
    #top.resizable(width=False, height=False)
    Application(top).mainloop()
