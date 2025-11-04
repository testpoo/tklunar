#!/usr/bin/env python3
# coding=utf-8

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import calendar
import re
from lunardata import *

class Calendar:
    def __init__(self):
        # 初始化当前日期
        self.current_date = date.today()
        self.selected_date = self.current_date
        self.cdate,self.clunar,self.cweek,self.cday = show_month(datetime.now().year, datetime.now().month, datetime.now().day)

        # 创建主窗口
        self.window = Gtk.Window(title="日历")
        self.window.set_default_size(530, 550)
        self.window.connect("destroy", Gtk.main_quit)
        self.window.set_icon_from_file("calendar.svg")

        # 创建主布局
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.window.add(self.main_box)

        # 创建标签栏
        self.label_box = Gtk.Box(spacing=20)
        self.main_box.pack_start(self.label_box, False, False, 1)

        # 公历日期
        self.date_label = Gtk.Label(label=str(self.cdate))
        self.date_label.set_size_request(250,50)
        self.date_label.set_justify(Gtk.Justification.CENTER)
        self.date_label.set_name("date_label")
        self.label_box.pack_start(self.date_label, False, False, 0)

        # 农历日期
        self.lunar_label = Gtk.Label(label=str(self.clunar))
        self.lunar_label.set_size_request(250,50)
        self.lunar_label.set_justify(Gtk.Justification.CENTER)
        self.lunar_label.set_name("lunar_label")
        self.label_box.pack_start(self.lunar_label, False, False, 0)

        # 创建按钮栏
        self.button_box = Gtk.Box(spacing=20)
        self.main_box.pack_start(self.button_box, False, False, 0)

        # 上一年按钮
        self.prev_year_button = Gtk.Button(label="◀")
        self.prev_year_button.connect("clicked", self.on_prev_year_clicked)
        self.prev_year_button.get_style_context().add_class('flat')
        self.button_box.pack_start(self.prev_year_button, False, False, 10)

        # 年份
        self.year_label = Gtk.Label(label=str(self.current_date.year))
        self.year_label.set_justify(Gtk.Justification.CENTER)
        self.button_box.pack_start(self.year_label, False, False, 0)

        # 下一年按钮
        self.next_year_button = Gtk.Button(label="▶")
        self.next_year_button.connect("clicked", self.on_next_year_clicked)
        self.next_year_button.get_style_context().add_class('flat')
        self.button_box.pack_start(self.next_year_button, False, False, 10)

        # 上一个月按钮
        self.prev_month_button = Gtk.Button(label="◀")
        self.prev_month_button.connect("clicked", self.on_prev_month_clicked)
        self.prev_month_button.get_style_context().add_class('flat')
        self.button_box.pack_start(self.prev_month_button, False, False, 10)

        # 月份
        self.month_label = Gtk.Label(label=str(self.current_date.month))
        self.month_label.set_justify(Gtk.Justification.CENTER)
        self.button_box.pack_start(self.month_label, False, False, 0)

        # 下一个月按钮
        self.next_month_button = Gtk.Button(label="▶")
        self.next_month_button.connect("clicked", self.on_next_month_clicked)
        self.next_month_button.get_style_context().add_class('flat')
        self.button_box.pack_start(self.next_month_button, False, False, 10)

        # 今天按钮
        self.today_button = Gtk.Button(label="今天")
        self.today_button.connect("clicked", self.on_today_clicked)
        self.today_button.get_style_context().add_class('flat')
        self.button_box.pack_start(self.today_button, False, False, 10)

        # 创建日历网格
        self.create_calendar_grid(self.cday)

        # 显示所有组件
        self.window.show_all()

    def create_calendar_grid(self,cday):

        """创建日历网格视图"""
        # 移除已有的日历网格（如果存在）
        if hasattr(self, 'calendar_grid'):
            self.main_box.remove(self.calendar_grid)

        # 创建新的网格
        self.calendar_grid = Gtk.Grid(column_spacing=1, row_spacing=1)
        self.main_box.pack_start(self.calendar_grid, True, True, 0)

        # 设置网格样式
        self.calendar_grid.set_border_width(0)

        # 绘制星期标题
        for i, day in enumerate(self.cweek):
            label = Gtk.Label(label="周"+day)
            label.set_halign(Gtk.Align.CENTER)
            label.set_valign(Gtk.Align.CENTER)
            label.set_name("weekday-label")
            self.calendar_grid.attach(label, i, 0, 1, 1)
            label.set_size_request(75, 50)

        # 获取当前月份数据
        year = self.current_date.year
        month = self.current_date.month

        # 绘制日期按钮
        for i in range(len(self.cday)):
            m,n = divmod(i,7)
            # 创建日期按钮
            if self.cday[i].split('\n')[0] == str(datetime.now().day) and self.current_date.month == datetime.now().month and self.current_date.year == datetime.now().year:
                btn = Gtk.Button(label=str(self.cday[i]))
                btn.set_name("today")
            elif self.cday[i][0] == '♩':
                btn = Gtk.Button(label=str(self.cday[i][1:]))
                btn.set_name("pre_month")
                # 绑定点击事件
                btn.connect("clicked", self.on_prev_month_clicked)
            elif self.cday[i][0] == '♪':
                btn = Gtk.Button(label=str(self.cday[i][1:]))
                btn.set_name(f"solarterms")
            elif self.cday[i][0] == '♫':
                btn = Gtk.Button(label=str(self.cday[i][1:]))
                btn.set_name(f"festival")
            elif self.cday[i][0] == '♬':
                btn = Gtk.Button(label=str(self.cday[i][1:]))
                btn.set_name(f"next_month")
                # 绑定点击事件
                btn.connect("clicked", self.on_next_month_clicked)
            else:
                btn = Gtk.Button(label=str(self.cday[i]))
                btn.set_name(f"day-btn-{self.cday[i]}")
                # 绑定点击事件
                btn.connect("clicked", self.on_day_clicked, year, month, int(self.cday[i].split('\n')[0]))
            date_btn = btn.get_child()
            date_btn.set_line_wrap(True)
            date_btn.set_justify(Gtk.Justification.CENTER)
            btn.get_style_context().add_class('flat')
            btn.set_halign(Gtk.Align.CENTER)
            btn.set_valign(Gtk.Align.CENTER)
            btn.set_size_request(75, 75)

            # 标记选中的日期
            if (self.selected_date.year == year and
                self.selected_date.month == month and
                self.selected_date.day == day):
                btn.get_style_context().add_class("selected")

            self.calendar_grid.attach(btn, n, m+1, 1, 1)

        # 应用CSS样式
        css_provider = Gtk.CssProvider()
        css = """
            #weekday-label {
                font-weight: bold;
                font-size: 14px;
            }
            #next_month,#pre_month {
                color: rgba(168,168,168,1.00);
            }
            #festival {
                color: rgba(231,73,62,1.00);
            }
            #solarterms {
                color: rgba(0,120,215,1.00);
            }
            #today {
                color: white;
                background: rgba(0,120,215,1.00);
                font-weight: bold;
            }
            .selected {
                background-color: #a8d1ff;
            }
            button {
                border-radius: 0px;
            }
            button:focus {
                outline: none;
            }
            #lunar_label, #date_label {
                color: rgba(0,120,215,1.00);
                font-weight: bold;
            }
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # 显示日历网格
        self.calendar_grid.show_all()

    def on_prev_year_clicked(self, widget):
        """切换到上一年"""
        self.current_date = self.current_date.replace(year=self.current_date.year - 1)
        self.year_label.set_text(str(self.current_date.year))
        self.cday = show_month(self.current_date.year, self.current_date.month, self.current_date.day)[-1]
        self.create_calendar_grid(self.cday)

    def on_next_year_clicked(self, widget):
        """切换到下一年"""
        self.current_date = self.current_date.replace(year=self.current_date.year + 1)
        self.year_label.set_text(str(self.current_date.year))
        self.cday = show_month(self.current_date.year, self.current_date.month, self.current_date.day)[-1]
        self.create_calendar_grid(self.cday)

    def on_prev_month_clicked(self, widget):
        """切换到上一个月"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
            self.year_label.set_text(str(self.current_date.year))
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.month_label.set_text(str(self.current_date.month))
        self.cday = show_month(self.current_date.year, self.current_date.month, self.current_date.day)[-1]
        self.create_calendar_grid(self.cday)

    def on_next_month_clicked(self, widget):
        """切换到下一个月"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
            self.year_label.set_text(str(self.current_date.year))
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.month_label.set_text(str(self.current_date.month))
        self.cday = show_month(self.current_date.year, self.current_date.month, self.current_date.day)[-1]
        self.create_calendar_grid(self.cday)

    def on_today_clicked(self, widget):
        """切换到今天"""
        self.current_date = date.today()
        self.selected_date = self.current_date
        self.year_label.set_text(str(self.current_date.year))
        self.month_label.set_text(str(self.current_date.month))
        self.cday = show_month(self.current_date.year, self.current_date.month, self.current_date.day)[-1]
        self.create_calendar_grid(self.cday)

    def on_day_clicked(self, widget, year, month, day):
        """选择日期"""
        self.selected_date = date(year, month, day)
        self.cday = show_month(self.current_date.year, self.current_date.month, self.current_date.day)[-1]
        self.create_calendar_grid(self.cday)

if __name__ == "__main__":
    app = Calendar()
    Gtk.main()
