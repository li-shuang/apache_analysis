# -*- coding: utf-8 -*-

import unittest
import sys
from common.data_analysis import ApacheAnalysis
from common.data_load import DataBase
from common.param_analysis import apache_param_analysis

mock_ips = ['177.1.81.42', '200.200.76.130']
mock_ip_visit_count = [3, 36]
mock_ip_article_count = [3,3]
log_file = 'log.txt'
server_ip = '123.206.195.94'
reoprt_type = 'all'


class ApacheTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ApacheTest, self)
    def setUp(self):
        pass
        
    def test_all_report(self):
        sys.argv[1] = server_ip
        sys.argv[2] = log_file
        sys.argv[3] = reoprt_type

        test_param = apache_param_analysis()
        test_data_base = DataBase()
        log_file_data = test_data_base.read_log_file(test_param['log_file'])
        test_apache_analysis = ApacheAnalysis(test_param['server_ip'])

        detailed_data_list = test_apache_analysis.get_detailed_data(log_file_data)
        data_set = test_apache_analysis.get_ip_url_set_data(detailed_data_list)
        test_apache_analysis.get_all_url_title_data(data_set)

        object_all = test_apache_analysis.get_all_report(detailed_data_list,data_set)
        object_ip = object_all['object_ip']
        ip_report_rows = object_ip._rows
        self.assertEquals(len(ip_report_rows), 2)
        for url_info in ip_report_rows:
            self.assertIn(url_info[0], mock_ips)
            self.assertIn(url_info[1], mock_ip_visit_count)
            self.assertIn(url_info[2], mock_ip_article_count)

#test = ApacheTest()
#test.test_all_report()
if __name__ == '__main__':
    unittest.main()