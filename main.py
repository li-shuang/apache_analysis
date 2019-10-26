# -*- coding: utf-8 -*-

from common.data_analysis import ApacheAnalysis
from common.data_load import DataBase
from tool.param_analysis import apache_param_analysis

if __name__ == '__main__':
    test_param = apache_param_analysis()
    test_data_base = DataBase()
    log_file_data = test_data_base.read_log_file(test_param['log_file_path'])
    test_apache_analysis = ApacheAnalysis(test_param['server_ip'])
    
    detailed_data_list = test_apache_analysis.get_detailed_data(log_file_data)
    data_set = test_apache_analysis.get_ip_url_set_data(detailed_data_list)
    test_apache_analysis.get_all_url_title_data(data_set)
    
    if test_param['report_type'] == 'ip' :
        test_apache_analysis.get_ip_report(detailed_data_list,data_set)

    if test_param['report_type'] == 'title' :
        test_apache_analysis.get_title_report(detailed_data_list,data_set)

    if test_param['report_type'] == 'full' :
        test_apache_analysis.get_full_report(detailed_data_list,data_set)

    if test_param['report_type'] == 'all' :
        test_apache_analysis.get_all_report(detailed_data_list,data_set)
