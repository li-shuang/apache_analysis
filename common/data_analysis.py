# -*- coding: utf-8 -*-
import re
import common.data_load
from tool.log import logger
import urllib2
from bs4 import BeautifulSoup
from prettytable import PrettyTable


class ApacheAnalysis(object):
    def __init__(self, host_ip):
        self.host_ip = host_ip
        self.all_url_title_data = {}

    def get_ip_url(self, data):
        """
        将log日志中的ip、时间、请求方法和url等重要信息提取
        :param data:log文件中的每行日志信息
        :return:{
                    "ip": 200.200.76.130,
                    "datetime": 16/Feb/2019:11:27:20 +0800,
                    "url":/coding/miniprj/material.html,
                    "method":GET
                }
        """
        REGEX = r'(?P<ip>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) - - ' \
                r'\[(?P<datetime>[^\]]+)\] "(?P<method>\w{3,9})' \
                r' (?P<url>[^\s]+) (?P<protocol>HTTP/\d\.\d)" ' \
                r'(?P<status>[0-9]{3})'

        res = re.search(REGEX, data)
        if res:
            return {"ip":res.group('ip'),
                    "datetime":res.group('datetime'),
                    "method":res.group('method'),
                    "url":res.group('url')}
        else:
            return None

    def get_url_html(self, url):
        """
        根据具体的url获取该页面的html信息
        :param url:
        :return:html:页面的html信息
        """
        logger.info("start get %(url)s html" % {'url': url})
        response = None

        try:
            response = urllib2.urlopen(url, timeout=1)
            html = response.read()
        except Exception as ex:
            logger.info("start get %(url)s html err:%(err)s" % {'url': url, 'err':ex})
            # 出现异常，直接返回None，不中断程序
            return None
        finally:
            if response:
                response.close()

        return html
    
    def get_html_title(self,url):
        """
        根据具体的url获取该页面的标题信息
        :param url:http://200.200.1.35//coding/miniprj/material.html
        :return:title:训练素材
        """
        html = self.get_url_html(url)
        
        if html is None:
            return None

        soup = BeautifulSoup(html, 'html.parser')
        node = getattr(soup, 'title')
        
        try:
            title = node.string
        except Exception as ex:
            logger.info(" title to string err:%(err)s" % {'err':ex})
            # 获取不到标题信息时，直接返回node信息
            return node

        return title

    def get_all_url_title_data(self, data_set):
        """
        提取所有的url的标题信息
        :param data_set:
        :return:{
                    "/coding/miniprj/material.html":训练素材,
                    "/designing/tools/image/gitbook/images/favicon.ic":None
                }
        """
        for title in data_set['title_url_set']:
            req_url = 'http://'+ self.host_ip + title
            article_title = self.get_html_title(req_url)
            self.all_url_title_data[title] = article_title

    def get_detailed_data(self,log_file_data):
        """
        将log文件中的列表数据整理，返回列表中包含字典的形式
        :param log_file_data:[
                                '200.200.76.130--[16/Feb/2019: 11: 27: 20+0800]"GET /coding/miniprj/material.html HTTP/1.1"20038093',
                                '200.200.76.130--[16/Feb/2019: 11: 27: 20+0800]"GET /coding/gitbook/gitbook-plugin-search-plus/search.css HTTP/1.1"2001095',
                                '200.200.76.130--[16/Feb/2019: 11: 27: 20+0800]"GET /coding/gitbook/gitbook-plugin-disqus/plugin.css HTTP/1.1"20063',
                                '200.200.76.130--[16/Feb/2019: 11: 27: 20+0800]"GET /coding/gitbook/gitbook-plugin-prism/prism-base16-ateliersulphurpool.light.css HTTP/1.1"2003290'
                            ]
        :return:[{
                    'url': '/coding/miniprj/material.html',
                    'ip': '200.200.76.130',
                    'method': 'GET',
                     'datetime': '16/Feb/2019: 11: 27: 20+0800'
                    },
                    {
                    'url': '/coding/gitbook/gitbook-plugin-search-plus/search.css',
                    'ip': '200.200.76.130',
                    'method': 'GET',
                    'datetime': '16/Feb/2019: 11: 27: 20+0800'
                    }]
        """
        detailed_data_list = []

        for data in log_file_data:
            data_info = self.get_ip_url(data)
            if data_info is not None:
                detailed_data_list.append(data_info)

        return detailed_data_list

    def get_ip_url_set_data(self,detailed_data_list):
        """
        提取所有的ip、title_url和ip_url等信息，去掉重复的数据,得到集合
        :param detailed_data_list:
        :return:{
                    "ip_set":ip_set,
                    "title_url_set":title_url_set, 
                    "ip_url_set":ip_url_set
                }
        """
        ip_set = set([])
        title_url_set = set([])
        ip_url_set = set([])
        
        for data in detailed_data_list:
            ip_set.add(data['ip'])
            html_url = data['url'].split("/")
            if ".js" in html_url[-1]:
                pass
            elif ".css" in html_url[-1]:
                pass
            else:
                # 将ip和url拼接起来，并用'+'进行连接，方便后续分割
                title_url_set.add(data['url'])
                ip_url = data['ip'] + '+' + data['url']
                ip_url_set.add(ip_url)

        return {"ip_set":ip_set,"title_url_set":title_url_set, "ip_url_set":ip_url_set}
                
    def get_ip_report(self, detailed_data_list, data_set):
        """
        获取IP报表
        :param detailed_data_list:[{
                                    'url': '/coding/miniprj/material.html',
                                    'ip': '200.200.76.130',
                                    'method': 'GET',
                                    'datetime': '16/Feb/2019: 11: 27: 20+0800'
                                    },
                                    {
                                    'url': '/coding/gitbook/gitbook-plugin-search-plus/search.css',
                                    'ip': '200.200.76.130',
                                    'method': 'GET',
                                    'datetime': '16/Feb/2019: 11: 27: 20+0800'
                                    }]
        :param data_set：
        :return:
        """
        tb = PrettyTable()
        tb.field_names = ["IP", "访问次数", "访问文章数"]
        
        for ip in data_set['ip_set']:
            visit_count = 0
            visit_title_count = 0
            for data in detailed_data_list:
                if ip == data['ip']:
                    visit_count = visit_count + 1
                    html_url = data['url'].split("/")
                    if ".js" in html_url[-1]:
                        pass
                    elif ".css" in html_url[-1]:
                        pass
                    else:
                        visit_title_count = visit_title_count + 1
            tb.add_row([ip, visit_count, visit_title_count])

        print(tb)
        return tb

    def get_title_report(self, detailed_data_list, data_set):
        """
        获取文章报表
        :param detailed_data_list:[{
                                    'url': '/coding/miniprj/material.html',
                                    'ip': '200.200.76.130',
                                    'method': 'GET',
                                    'datetime': '16/Feb/2019: 11: 27: 20+0800'
                                    },
                                    {
                                    'url': '/coding/gitbook/gitbook-plugin-search-plus/search.css',
                                    'ip': '200.200.76.130',
                                    'method': 'GET',
                                    'datetime': '16/Feb/2019: 11: 27: 20+0800'
                                    }]
        :param data_set：
        :return:
        """
        tb = PrettyTable()
        tb.field_names = ["URL", "文章标题", "访问人次", "访问IP数"]

        for title in data_set['title_url_set']:
            visit_count = 0
            ip_visit_count = 0
            title_ip_set = set([])
            for data in detailed_data_list:
                if title == data['url']:
                    visit_count = visit_count + 1
                    title_ip_set.add(data['ip'])
            ip_visit_count = len(title_ip_set)
            req_url = 'http://'+ self.host_ip + title
            article_title = self.get_html_title(req_url)
            tb.add_row([title, article_title, visit_count, ip_visit_count])

        print(tb)
        return tb
            
    def get_full_report(self, detailed_data_list, data_set):
        """
        获取完整报表
        :param detailed_data_list:[{
                                    'url': '/coding/miniprj/material.html',
                                    'ip': '200.200.76.130',
                                    'method': 'GET',
                                    'datetime': '16/Feb/2019: 11: 27: 20+0800'
                                    },
                                    {
                                    'url': '/coding/gitbook/gitbook-plugin-search-plus/search.css',
                                    'ip': '200.200.76.130',
                                    'method': 'GET',
                                    'datetime': '16/Feb/2019: 11: 27: 20+0800'
                                    }]
        :param data_set：
        :return:
        """
        tb = PrettyTable()
        tb.field_names = ["IP", "URL", "访问次数"]

        for ip_url in data_set['ip_url_set']:
            visit_count = 0
            for data in detailed_data_list:
                data_ip_url = data['ip'] + '+' + data['url']
                if ip_url == data_ip_url :
                    visit_count = visit_count + 1
            ip_url = ip_url.split("+")
            ip = ip_url[0]
            url = ip_url[1]
            tb.add_row([ip, url, visit_count])

        print(tb)
        return tb
        
    def get_all_report(self, detailed_data_list, data_set):
        """
        获取所有的报表
        :param detailed_data_list:[{
                                    'url': '/coding/miniprj/material.html',
                                    'ip': '200.200.76.130',
                                    'method': 'GET',
                                    'datetime': '16/Feb/2019: 11: 27: 20+0800'
                                    },
                                    {
                                    'url': '/coding/gitbook/gitbook-plugin-search-plus/search.css',
                                    'ip': '200.200.76.130',
                                    'method': 'GET',
                                    'datetime': '16/Feb/2019: 11: 27: 20+0800'
                                    }]
        :param data_set：
        :return:
        """
        object_title = self.get_title_report(detailed_data_list, data_set)
        object_ip = self.get_ip_report(detailed_data_list, data_set)
        object_full = self.get_full_report(detailed_data_list, data_set)

        return {"object_title":object_title, "object_ip":object_ip, "object_full":object_full}  
