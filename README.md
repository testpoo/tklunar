# xfce-lunar
桌面版农历日历，支持Linux

### 依赖
```
python3-gi
```

### 运行
```
# 无参数表示正常日历，有菜单栏和任务栏
python3 xflunar.py

# 有参数表示传统模式，没有菜单栏和任务栏
python3 xflunar.py rightbottom # 位置右下
python3 xflunar.py upperright  # 位置右上
python3 xflunar.py upperleft   # 位置左上
python3 xflunar.py bottomleft  # 位置左下
python3 xflunar.py middle      # 除上面四个值外，其他值都居中

# 安装deb包直接执行xflunar或xflunar加参数即可
```

### 展示
![linux](linux.png)

### 注意
- 在debian13/testing xfce4.20桌面下测试通过，理论上来说其他有python3环境的Linux桌面也可以使用。
