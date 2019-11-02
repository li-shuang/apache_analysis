# -*- coding: utf-8 -*-

import unittest
import sys
from common.data_analysis import ApacheAnalysis
from common.data_load import DataBase

mock_ip_ips = ['177.1.81.42', '200.200.76.130']
mock_ip_visit_count = [3, 36]
mock_ip_article_count = [3,3]

mock_title_urls = [
    '/coding/miniprj/material.html',
    '/designing/tools/image/UML_classes.docx',
    '/designing/tools/image/gitbook/images/favicon.ico',
    '/coding/gitbook/fonts/fontawesome/fontawesome-webfont.woff2?v=4.6.3',
    '/designing/tools/image/favicon.ico',
    '/coding/style/%E7%BC%96%E7%A0%81%E9%A3%8E%E6%A0%BC.zip'
]

'''mock_title_arttitle = [
    '训练素材',
    None,
    None,
    None,
    None,
    None
]'''

mock_title_visit_count = [1, 1, 1, 1, 1, 1]
mock_title_ip_count = [1, 1, 1, 1, 1, 1]

mock_full_ips = [
    '200.200.76.130',
    '200.200.76.130',
    '200.200.76.130',
    '177.1.81.42',
    '177.1.81.42',
    '177.1.81.42'
]

mock_full_urls = [
    '/coding/gitbook/fonts/fontawesome/fontawesome-webfont.woff2?v=4.6.3',
    '/coding/miniprj/material.html',
    '/coding/style/%E7%BC%96%E7%A0%81%E9%A3%8E%E6%A0%BC.zip',
    '/designing/tools/image/gitbook/images/favicon.ico',
    '/designing/tools/image/UML_classes.docx',
    '/designing/tools/image/favicon.ico'
]
mock_full_visit = [1, 1, 1, 1, 1, 1]

test_log_file_data = [
    '200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/miniprj/material.html HTTP/1.1" 200 38093',
    '200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/gitbook/gitbook-plugin-search-plus/search.css HTTP/1.1" 200 1095'
]

test_detailed_data_list = [
    {
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
    }
]

test_check_false_data_set = {
    "ip_set":set(['200.200.76.130']),
    "title_url_set":set(['/coding/miniprj/material.html',
                     '/coding/gitbook/gitbook-plugin-search-plus/search.css'
                     ]),
    "ip_url_set":set(['200.200.76.130+/coding/miniprj/material.html',
                  '200.200.76.130+/coding/gitbook/gitbook-plugin-search-plus/search.css'
                  ])
}

test_check_true_data_set = {
    "ip_set":set(['200.200.76.130']),
    "title_url_set":set(['/coding/miniprj/material.html',]),
    "ip_url_set":set(['200.200.76.130+/coding/miniprj/material.html'])
}
log_file = 'log.txt'
err_log_file = '/xxx/xxx/log.txt'
server_ip = '200.200.1.35'
reoprt_type = 'all'
test_true_url = '/coding/miniprj/material.html'
test_false_url = '/lishhuang/xxxx.html'


class ApacheTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ApacheTest, self).__init__(*args, **kwargs)

    def setUp(self):
        pass

    def test_read_log_file(self):
        test_base = DataBase()
        try:
            self.assertRaises(Exceptioan, test_base.read_log_file(err_log_file))
        except:
            pass
        test_log_file = test_base.read_log_file(log_file)
        self.assertIsNotNone(test_log_file)

    def test_get_ip_url(self):
        test_data = '200.200.76.130 - - [16/Feb/2019:11:27:20 +0800] "GET /coding/miniprj/material.html HTTP/1.1" 200 38093'

        test_url_object = ApacheAnalysis(server_ip)
        check_data = {
                    "ip": '200.200.76.130',
                    "datetime": '16/Feb/2019:11:27:20 +0800',
                    "url":'/coding/miniprj/material.html',
                    "method":'GET'
                }
        test_obj = test_url_object.get_ip_url(test_data)
        self.assertEqual(test_obj, check_data)

        test_obj = test_url_object.get_ip_url("xxxxxxxxxx")
        self.assertEqual(None, test_obj)
    
    def test_get_url_html(self):
        test_html_object = ApacheAnalysis(server_ip)
        #test_html_object.get_url_html(test_true_url)
        test_false_object = test_html_object.get_url_html(test_false_url)
        self.assertEqual(None, test_false_object)

    def test_get_all_url_title_data(self):
        test_all_url_title_object = ApacheAnalysis(server_ip)
        test_all_url_title_object.get_all_url_title_data(test_check_true_data_set)
        check_all_url_title_data = {
                    "/coding/miniprj/material.html":None
                }
        self.assertEqual(check_all_url_title_data,test_all_url_title_object.all_url_title_data)

    def test_get_ip_url_set_data(self):
        test_data_set_object = ApacheAnalysis(server_ip)
        test_data_set = test_data_set_object.get_ip_url_set_data(test_detailed_data_list)
        self.assertNotEqual(test_check_false_data_set, test_data_set)
        self.assertEqual(test_check_true_data_set, test_data_set)

    def test_get_html_title(self):
        test_html_title_object = ApacheAnalysis(server_ip)
        test_url = 'http://' + server_ip + test_true_url
        test_true_title = test_html_title_object.get_html_title(test_url)
        check_true_title = None
        self.assertEqual(check_true_title, test_true_title)
        test_false_title = test_html_title_object.get_html_title(test_false_url)
        check_false_title = None
        self.assertEqual(check_false_title, test_false_title)

    def test_get_detailed_data(self):
        test_get_detailed_data_object = ApacheAnalysis(server_ip)
        detailed_data = test_get_detailed_data_object.get_detailed_data(test_log_file_data)
        check_detailed_data = [
            {
                'url': '/coding/miniprj/material.html',
                'ip': '200.200.76.130',
                'method': 'GET',
                'datetime': '16/Feb/2019:11:27:20 +0800'},
            {
                'url': '/coding/gitbook/gitbook-plugin-search-plus/search.css',
                'ip': '200.200.76.130',
                'method': 'GET',
                'datetime': '16/Feb/2019:11:27:20 +0800'
            }
        ]
        self.assertEqual(check_detailed_data, detailed_data)

    def test_all_report(self):
        test_data_base = DataBase()
        log_file_data = test_data_base.read_log_file(log_file)
        test_apache_analysis = ApacheAnalysis(server_ip)

        detailed_data_list = test_apache_analysis.get_detailed_data(log_file_data)
        data_set = test_apache_analysis.get_ip_url_set_data(detailed_data_list)
        test_apache_analysis.get_all_url_title_data(data_set)

        object_all = test_apache_analysis.get_all_report(detailed_data_list,data_set)

        # 测试文章报表
        object_title = object_all['object_title']
        title_report_rows = object_title._rows
        self.assertEquals(len(title_report_rows), 6)
        for url_info in title_report_rows:
            self.assertIn(url_info[0], mock_title_urls)
            #self.assertIn(url_info[1], mock_title_arttitle)
            self.assertIn(url_info[2], mock_title_visit_count)
            self.assertIn(url_info[3], mock_title_ip_count)
        # 测试完整报表
        object_full = object_all['object_full']
        full_report_rows = object_full._rows
        self.assertEquals(len(full_report_rows), 6)
        for url_info in full_report_rows:
            self.assertIn(url_info[0], mock_full_ips)
            self.assertIn(url_info[1], mock_full_urls)
            self.assertIn(url_info[2], mock_title_visit_count)
        
        # 测试ip报表的正确性
        object_ip = object_all['object_ip']
        ip_report_rows = object_ip._rows
        self.assertEquals(len(ip_report_rows), 2)
        for url_info in ip_report_rows:
            self.assertIn(url_info[0], mock_ip_ips)
            self.assertIn(url_info[1], mock_ip_visit_count)
            self.assertIn(url_info[2], mock_ip_article_count)

if __name__ == '__main__':
    unittest.main()