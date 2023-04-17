#!/usr/bin/env python3
# coding=utf-8

from datetime import date, datetime
import calendar
import itertools
from solarterms import *

__author__ = {'name' : 'TestPoo', 'created' : '2022-05-05'}

#####################################################################################
# 1901~2100年农历数据表 # powered by Late Lee
# 农历数据 每个元素的存储格式如下： # 16~13 12 11~0 闰几月 闰月日数 1~12月份农历日数 
# 1、bit0表示农历1月份日数，为1表示30天，为0表示29天。bit1表示农历2月份日数，依次类推。 
# 2、bit12表示闰月日数，1为30天，0为29天。bit17~bit14表示第几月是闰月(注：为0表示该年无闰月) 
# 数据来源: http://data.weather.gov.hk/gts/time/conversion1_text_c.htm
#####################################################################################

g_lunar_month_day = [
 0x00752, 0x00ea5, 0x0ab2a, 0x0064b, 0x00a9b, 0x09aa6, 0x0056a, 0x00b59, 0x04baa, 0x00752, # 1901 ~ 1910 
 0x0cda5, 0x00b25, 0x00a4b, 0x0ba4b, 0x002ad, 0x0056b, 0x045b5, 0x00da9, 0x0fe92, 0x00e92, # 1911 ~ 1920 
 0x00d25, 0x0ad2d, 0x00a56, 0x002b6, 0x09ad5, 0x006d4, 0x00ea9, 0x04f4a, 0x00e92, 0x0c6a6, # 1921 ~ 1930 
 0x0052b, 0x00a57, 0x0b956, 0x00b5a, 0x006d4, 0x07761, 0x00749, 0x0fb13, 0x00a93, 0x0052b, # 1931 ~ 1940 
 0x0d51b, 0x00aad, 0x0056a, 0x09da5, 0x00ba4, 0x00b49, 0x04d4b, 0x00a95, 0x0eaad, 0x00536, # 1941 ~ 1950 
 0x00aad, 0x0baca, 0x005b2, 0x00da5, 0x07ea2, 0x00d4a, 0x10595, 0x00a97, 0x00556, 0x0c575, # 1951 ~ 1960 
 0x00ad5, 0x006d2, 0x08755, 0x00ea5, 0x0064a, 0x0664f, 0x00a9b, 0x0eada, 0x0056a, 0x00b69, # 1961 ~ 1970 
 0x0abb2, 0x00b52, 0x00b25, 0x08b2b, 0x00a4b, 0x10aab, 0x002ad, 0x0056d, 0x0d5a9, 0x00da9, # 1971 ~ 1980 
 0x00d92, 0x08e95, 0x00d25, 0x14e4d, 0x00a56, 0x002b6, 0x0c2f5, 0x006d5, 0x00ea9, 0x0af52, # 1981 ~ 1990 
 0x00e92, 0x00d26, 0x0652e, 0x00a57, 0x10ad6, 0x0035a, 0x006d5, 0x0ab69, 0x00749, 0x00693, # 1991 ~ 2000 
 0x08a9b, 0x0052b, 0x00a5b, 0x04aae, 0x0056a, 0x0edd5, 0x00ba4, 0x00b49, 0x0ad53, 0x00a95, # 2001 ~ 2010 
 0x0052d, 0x0855d, 0x00ab5, 0x12baa, 0x005d2, 0x00da5, 0x0de8a, 0x00d4a, 0x00c95, 0x08a9e, # 2011 ~ 2020 
 0x00556, 0x00ab5, 0x04ada, 0x006d2, 0x0c765, 0x00725, 0x0064b, 0x0a657, 0x00cab, 0x0055a, # 2021 ~ 2030 
 0x0656e, 0x00b69, 0x16f52, 0x00b52, 0x00b25, 0x0dd0b, 0x00a4b, 0x004ab, 0x0a2bb, 0x005ad, # 2031 ~ 2040 
 0x00b6a, 0x04daa, 0x00d92, 0x0eea5, 0x00d25, 0x00a55, 0x0ba4d, 0x004b6, 0x005b5, 0x076d2, # 2041 ~ 2050 
 0x00ec9, 0x10f92, 0x00e92, 0x00d26, 0x0d516, 0x00a57, 0x00556, 0x09365, 0x00755, 0x00749, # 2051 ~ 2060 
 0x0674b, 0x00693, 0x0eaab, 0x0052b, 0x00a5b, 0x0aaba, 0x0056a, 0x00b65, 0x08baa, 0x00b4a, # 2061 ~ 2070 
 0x10d95, 0x00a95, 0x0052d, 0x0c56d, 0x00ab5, 0x005aa, 0x085d5, 0x00da5, 0x00d4a, 0x06e4d, # 2071 ~ 2080 
 0x00c96, 0x0ecce, 0x00556, 0x00ab5, 0x0bad2, 0x006d2, 0x00ea5, 0x0872a, 0x0068b, 0x10697, # 2081 ~ 2090 
 0x004ab, 0x0055b, 0x0d556, 0x00b6a, 0x00752, 0x08b95, 0x00b45, 0x00a8b, 0x04a4f, ]


#农历数据 每个元素的存储格式如下： 
# 12~7 6~5 4~0 
# 离元旦多少天 春节月 春节日 
#####################################################################################
g_lunar_year_day = [
 0x18d3, 0x1348, 0x0e3d, 0x1750, 0x1144, 0x0c39, 0x15cd, 0x1042, 0x0ab6, 0x144a, # 1901 ~ 1910 
 0x0ebe, 0x1852, 0x1246, 0x0cba, 0x164e, 0x10c3, 0x0b37, 0x14cb, 0x0fc1, 0x1954, # 1911 ~ 1920 
 0x1348, 0x0dbc, 0x1750, 0x11c5, 0x0bb8, 0x15cd, 0x1042, 0x0b37, 0x144a, 0x0ebe, # 1921 ~ 1930 
 0x17d1, 0x1246, 0x0cba, 0x164e, 0x1144, 0x0bb8, 0x14cb, 0x0f3f, 0x18d3, 0x1348, # 1931 ~ 1940 
 0x0d3b, 0x16cf, 0x11c5, 0x0c39, 0x15cd, 0x1042, 0x0ab6, 0x144a, 0x0e3d, 0x17d1, # 1941 ~ 1950 
 0x1246, 0x0d3b, 0x164e, 0x10c3, 0x0bb8, 0x154c, 0x0f3f, 0x1852, 0x1348, 0x0dbc, # 1951 ~ 1960 
 0x16cf, 0x11c5, 0x0c39, 0x15cd, 0x1042, 0x0a35, 0x13c9, 0x0ebe, 0x17d1, 0x1246, # 1961 ~ 1970 
 0x0d3b, 0x16cf, 0x10c3, 0x0b37, 0x14cb, 0x0f3f, 0x1852, 0x12c7, 0x0dbc, 0x1750, # 1971 ~ 1980 
 0x11c5, 0x0c39, 0x15cd, 0x1042, 0x1954, 0x13c9, 0x0e3d, 0x17d1, 0x1246, 0x0d3b, # 1981 ~ 1990 
 0x16cf, 0x1144, 0x0b37, 0x144a, 0x0f3f, 0x18d3, 0x12c7, 0x0dbc, 0x1750, 0x11c5, # 1991 ~ 2000 
 0x0bb8, 0x154c, 0x0fc1, 0x0ab6, 0x13c9, 0x0e3d, 0x1852, 0x12c7, 0x0cba, 0x164e, # 2001 ~ 2010 
 0x10c3, 0x0b37, 0x144a, 0x0f3f, 0x18d3, 0x1348, 0x0dbc, 0x1750, 0x11c5, 0x0c39, # 2011 ~ 2020 
 0x154c, 0x0fc1, 0x0ab6, 0x144a, 0x0e3d, 0x17d1, 0x1246, 0x0cba, 0x15cd, 0x10c3, # 2021 ~ 2030 
 0x0b37, 0x14cb, 0x0f3f, 0x18d3, 0x1348, 0x0dbc, 0x16cf, 0x1144, 0x0bb8, 0x154c, # 2031 ~ 2040 
 0x0fc1, 0x0ab6, 0x144a, 0x0ebe, 0x17d1, 0x1246, 0x0cba, 0x164e, 0x1042, 0x0b37, # 2041 ~ 2050 
 0x14cb, 0x0fc1, 0x18d3, 0x1348, 0x0dbc, 0x16cf, 0x1144, 0x0a38, 0x154c, 0x1042, # 2051 ~ 2060 
 0x0a35, 0x13c9, 0x0e3d, 0x17d1, 0x11c5, 0x0cba, 0x164e, 0x10c3, 0x0b37, 0x14cb, # 2061 ~ 2070 
 0x0f3f, 0x18d3, 0x12c7, 0x0d3b, 0x16cf, 0x11c5, 0x0bb8, 0x154c, 0x1042, 0x0ab6, # 2071 ~ 2080 
 0x13c9, 0x0e3d, 0x17d1, 0x1246, 0x0cba, 0x164e, 0x10c3, 0x0bb8, 0x144a, 0x0ebe, # 2081 ~ 2090 
 0x1852, 0x12c7, 0x0d3b, 0x16cf, 0x11c5, 0x0c39, 0x154c, 0x0fc1, 0x0a35, 0x13c9, # 2091 ~ 2100 
 ]

#==================================================================================

START_YEAR = 1901

month_DAY_BIT = 12
month_NUM_BIT = 13

yuefeng = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "冬月", "腊月"]
riqi = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
"十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "廿十",
"廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]

xingqi = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
shengxiao = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

def change_year(num):
    dx = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    tmp_str = ""
    for i in str(num):
        tmp_str += dx[int(i)]
    return tmp_str

def week_str(tm):
    return xingqi[tm.weekday()]

def lunar_day(day):
    return riqi[(day - 1) % 30]

def lunar_day1(month, day):
    if day == 1:
        return lunar_month(month)
    elif day == 31:
        return yuefeng[month]
    else:
        return riqi[day - 1]

def lunar_month(month):
    leap = (month>>4)&0xf
    m = month&0xf
    month = yuefeng[(m - 1) % 12]
    if leap == m:
        month = "闰" + month
    return month

def lunar_year(year):
    return tiangan[(year - 4) % 10] + dizhi[(year - 4) % 12] + '[' + shengxiao[(year - 4) % 12] + ']'

# 返回：
# a b c
# 闰几月，该闰月多少天 传入月份多少天
def lunar_month_days(lunar_year, lunar_month):
    if (lunar_year < START_YEAR):
        return 30

    leap_month, leap_day, month_day = 0, 0, 0 # 闰几月，该月多少天 传入月份多少天

    tmp = g_lunar_month_day[lunar_year - START_YEAR]

    if tmp & (1<<(lunar_month-1)):
        month_day = 30
    else:
        month_day = 29

    # 闰月
    leap_month = (tmp >> month_NUM_BIT) & 0xf
    if leap_month:
        if (tmp & (1<<month_DAY_BIT)):
            leap_day = 30
        else:
            leap_day = 29

    return (leap_month, leap_day, month_day)

# 算农历日期
# 返回的月份中，高4bit为闰月月份，低4bit为其它正常月份
def get_ludar_date(tm):
    year, month, day = tm.year, 1, 1
    code_data = g_lunar_year_day[year - START_YEAR]
    days_tmp = (code_data >> 7) & 0x3f
    chunjie_d = (code_data >> 0) & 0x1f
    chunjie_m = (code_data >> 5) & 0x3
    span_days = (tm - datetime(year, chunjie_m, chunjie_d)).days

    # 日期在该年农历之后
    if (span_days >= 0):
        (leap_month, foo, tmp) = lunar_month_days(year, month)
        while span_days >= tmp:
            span_days -= tmp
            if (month == leap_month):
                (leap_month, tmp, foo) = lunar_month_days(year, month) # 注：tmp变为闰月日数
                if (span_days < tmp): # 指定日期在闰月中
                    month = (leap_month<<4) | month
                    break
                span_days -= tmp
            month += 1 # 此处累加得到当前是第几个月
            (leap_month, foo, tmp) = lunar_month_days(year, month)
        day += span_days
        return year, month, day
    # 倒算日历
    else:
        month = 12
        year -= 1
        (leap_month, foo, tmp) = lunar_month_days(year, month)
        while abs(span_days) >= tmp:
            span_days += tmp
            month -= 1
            if (month == leap_month):
                (leap_month, tmp, foo) = lunar_month_days(year, month)
                if (abs(span_days) < tmp): # 指定日期在闰月中
                    month = (leap_month<<4) | month
                    break
                span_days += tmp
            (leap_month, foo, tmp) = lunar_month_days(year, month)
        day += (tmp + span_days) # 从月份总数中倒扣 得到天数
        return year, month, day

def pre_next(lists):
    listden = [len(list(v)) for k,v in itertools.groupby(lists)]
    if lists[0] == 0 and lists[-1] == 0:
        dspre = listden[0]
        dsnext = listden[-1]
    elif lists[0] == 0 and lists[-1] != 0:
        dspre = listden[0]
        dsnext = 0
    elif lists[0] != 0 and lists[-1] == 0:
        dspre = 0
        dsnext = listden[-1]
    else:
        dspre = 0
        dsnext = 0
    return dspre,dsnext

def add_solar_terms(year, month, day):
    jieqiss = jieqi()
    jieqis = jieqiss.get_year_jieqi(year)
    month = '%02d' % month
    day = '%02d' % day
    time = "-".join((str(year), str(month), str(day)))
    for jq in jieqis:
        if jq['time'][:10] == time:
            return jq['name']

def add_lunar_festival(year, month, day):
    lastday = ''
    if month == 12:
        tmp = g_lunar_month_day[year - START_YEAR]
        if tmp & (1<<(11)):
            lastday = '12-30'
        else:
            lastday = '12-29'
    festival_date = [{'name':'春节','date':'1-1'},{'name':'除夕','date':lastday},{'name':'元宵节','date':'1-15'},
                     {'name':'龙头节','date':'2-2'},{'name':'上巳节','date':'3-3'},{'name':'端午节','date':'5-5'},
                     {'name':'七夕节','date':'7-7'},{'name':'中元节','date':'7-15'},{'name':'中秋节','date':'8-15'},
                     {'name':'重阳节','date':'9-9'},{'name':'腊八节','date':'12-8'}
                    ]
    date = '-'.join((str(month), str(day)))
    for fest in festival_date:
        if fest['date'] == date:
            return fest['name']

def add_festival(month, day):
    festival_date = [{'name':'元旦','date':'1-1'},{'name':'妇女节','date':'3-8'},{'name':'劳动节','date':'5-1'},{'name':'国庆节','date':'10-1'}]
    date = '-'.join((str(month), str(day)))
    for fest in festival_date:
        if fest['date'] == date:
            return fest['name']

def show_month(year, month, day):
    if year > 2100 or year < 1901:
        return
    if month > 13 or month < 1:
        return

    tm = datetime(year, month, day)
    
    if tm.month < 10:
        tm_month = "0" + str(tm.month)
    else:
        tm_month = str(tm.month)

    (year, month, day) = get_ludar_date(tm)
    cdate = "".join((str(tm.year),"年",tm_month,"月",str(tm.day),"日"," ",str(week_str(tm))))
    clunar = "".join((lunar_year(year),"年"," ",change_year(year),"年",lunar_month(month),lunar_day(day))) # 根据数组索引确定
    cweek = ("一","二","三","四","五","六","日")

    c = calendar.Calendar(0)
    ds = [d for d in c.itermonthdays(tm.year, tm.month)]

    dspre,dsnext = pre_next(ds)

    cday = []

    if dspre > 0:
        tyear = tm.year
        tmonth = tm.month - 1
        if tmonth == 0:
            tyear = tyear - 1
            tmonth = 12
        dspre = [d for d in c.itermonthdays(tyear, tmonth) if d !=0][dspre*(-1):]
        for d in dspre:
            (year, month, day) = get_ludar_date(datetime(tyear, tmonth, d))
            if add_solar_terms(tyear, tmonth, d):
                cday.append('*' + str(d) + '\n' + add_solar_terms(tyear, tmonth, day))
            elif add_lunar_festival(year, month, day):
                cday.append('*' + str(d) + '\n' + add_lunar_festival(year,month, day))
            elif add_festival(tmonth, d):
                cday.append('*' + str(d) + '\n' + add_festival(tmonth, d))
            else:
                cday.append('*' + str(d) + '\n' + lunar_day1(month, day))

    for d in ds:
        if d != 0:
            (year, month, day) = get_ludar_date(datetime(tm.year, tm.month, d))
            if add_solar_terms(tm.year, tm.month, d):
                cday.append('$' + str(d) + '\n' + add_solar_terms(tm.year, tm.month, d))
            elif add_lunar_festival(year, month, day):
                cday.append('@' + str(d) + '\n' + add_lunar_festival(year,month, day))
            elif add_festival(tm.month, d):
                cday.append('@' + str(d) + '\n' + add_festival(tm.month, d))
            else:
                cday.append(str(d) + '\n' + lunar_day1(month, day))

    tyear = tm.year
    tmonth = tm.month + 1
    if tmonth == 13:
        tyear = tyear + 1
        tmonth = 1
    if len(cday) + dsnext < 42:
        dsnext = [d for d in c.itermonthdays(tyear, tmonth) if d !=0][0:42-len(cday)]
    else:
        dsnext = [d for d in c.itermonthdays(tyear, tmonth) if d !=0][0:dsnext]
    for d in dsnext:
        (year, month, day) = get_ludar_date(datetime(tyear, tmonth, d))
        if add_solar_terms(tyear, tmonth, d):
            cday.append('#' + str(d) + '\n' + add_solar_terms(tyear, tmonth, d))
        elif add_lunar_festival(year, month, day):
            cday.append('#' + str(d) + '\n' + add_lunar_festival(year,month, day))
        elif add_festival(tmonth, d):
            cday.append('#' + str(d) + '\n' + add_festival(tmonth, d))
        else:
            cday.append('#' + str(d) + '\n' + lunar_day1(month, day))

    return cdate,clunar,cweek,cday
