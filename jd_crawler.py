# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import matplotlib.pyplot as plt
# import numpy as np

# 抓取页面
def get_page( url ):
    req = urllib.request.Request(url)
    req.add_header( "User-Agent",
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/ 20100101 Firefox/66.0' )
    return urllib.request.urlopen(req, timeout=15).read()

if __name__ == "__main__":
    url = 'https://list.jd.com/list.html?cat=1713,3258,3304&page=1&sort=sort_totalsales15_desc&trans=1&JL=4_2_0#J_main'
    text = get_page(url)
    # 读取
    open("out.html","wb").write(text)
    # decode转换为字符串
    text = text.decode("utf-8")
    # 放入Beautiful解析
    root = BeautifulSoup(text, "html.parser")
    # 计算数量的字典
    author = {}
    # 寻找节点
    for item in root.find_all(class_= "author_type_1"):
        a = item.find("a").get_text()
        # 若作者不在字典中，就加入字典；若在其中，就将数量加一
        if a in author:
            author[a] += 1
        else:
            author[a] = 1
    # 排序存到author_s，并将数量为1的作者归类到“其他”
    author_s = {}
    count = 0
    for i in sorted(author,key=author.__getitem__):
        if author[i] == 1:
            count += 1
        else:
            author_s[i] = author[i]
    author_s['其他'] = count
    # 分离作者和作者数量
    y = [item for item in author_s]
    x = [author_s[a] for a in y]
    # 把“其他”放到列表首位，画图时会画在最下面
    a = x.pop()
    b = y.pop()
    x.insert(0, a)
    y.insert(0, b)

    fig,ax = plt.subplots(figsize=(10,6))  # 生成画布
    plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一，替换sans-serif字体
    plt.subplots_adjust(left=0.2, bottom=0.1, right=0.95, top=0.9)  # 设置间隔
    ax.grid(True, linestyle=':',color='grey',alpha=0.5)  # 设置格线
    plt.barh(y, x, height=0.8, align='center', color='b', alpha=0.6)  # 生成柱状图
    plt.xlabel("数量")  # x轴标签
    plt.ylabel("作家")  # y轴标签
    plt.title("京东侦探/悬疑/推理小说作家数量统计")  # 大标题
    plt.show()  # 绘制
    