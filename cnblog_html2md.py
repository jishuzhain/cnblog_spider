#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/10/12
# @Author  : jishuzhain
# @Link    :
# @Version : 1.0
# 图片需要绝对路径，或者直接下载图片到本地
# 采用多线程生成pdf文件

from __future__ import with_statement
import threading
import requests
from bs4 import BeautifulSoup
import html2text
import re
import time
import os
import pdfkit
# from PyPDF2 import PdfFileMerger
import sys
reload(sys)
sys.setdefaultencoding('utf8')

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
<h2>{title}</h2>
{content}
</body>
</html>

"""

path = "D:\\html2md\\skyblue-li"


def get_html():
    p = 0
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}

    for n in range(10, 0, -1):
        url = 'https://www.cnblogs.com/skyblue-li/default.html?page={}'.format(n)
        # url = 'https://www.cnblogs.com/skyblue-li/p/5900100.html'
        time.sleep(1)
        r = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        blog_list = soup.find_all(class_='postTitle')
        for i in blog_list:
            time.sleep(2)
            href = i.find('a').get('href')
            href_response = requests.get(href, headers=headers, verify=False)
            href_soup = BeautifulSoup(href_response.text, "html.parser")
            title = href_soup.find(class_='postTitle').text
            # if "JavaWeb" in title:
            print title
            body = href_soup.find(id='cnblogs_post_body')
            # body = re.sub(r'<img src="//', "", body)
            body = re.sub(r'<img.*?src="//', "<img src=\"https://", str(body))
            # content = str(body)
            title = str(title)
            html = html_template.format(content=body, title=title)
            if os.path.exists(path):
                with open(path + '\\' + str(p) + ".html", 'w') as f:
                    f.write(html)
            else:
                os.mkdir(path)

            html_content = open(path + '\\' + str(p) + ".html", 'rb')
            md_content = html2text.html2text(html_content.read().decode('utf-8', 'ignore').replace(u'\xa9', u''))

            with open(path + '\\' + str(p) + '.md', 'w') as f:
                f.write(md_content)
            p += 1
    return p


def save_pdf(htmls, file_name):
    """
    把所有html文件保存到pdf文件
    :param htmls:  html文件列表
    :param file_name: pdf文件名
    :return:
    """
    pdfkit.from_file(htmls, file_name)


def main():
    name = get_html()
    threads = []
    for i in range(0, name):
        t = threading.Thread(target=save_pdf, args=(path + '\\' + str(i) + '.html',path + '\\' + str(i) + '.pdf', ))
        threads.append(t)

    for i in range(0, name):
        threads[i].start()

    for i in range(0, name):
        threads[i].join()


if __name__ == "__main__":
    main()
