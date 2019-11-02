# -*- coding: utf-8 -*-

from common.data_analysis import ApacheAnalysis
from common.data_load import DataBase
from tool.param_analysis import apache_param_analysis

if __name__ == '__main__':
    # 参数检查
    param = apache_param_analysis()
    # 加载数据类
    data_base = DataBase()
    # 获取log文件中的数据
    log_file_data = data_base.read_log_file(param['log_file_path'])
    # 生成日志分析类，设定服务器ip
    apache_analysis = ApacheAnalysis(param['server_ip'])
    
    detailed_data_list = apache_analysis.get_detailed_data(log_file_data)
    data_set = apache_analysis.get_ip_url_set_data(detailed_data_list)
    apache_analysis.get_all_url_title_data(data_set)
    
    if param['report_type'] == 'ip' :
        apache_analysis.get_ip_report(detailed_data_list,data_set)

    if param['report_type'] == 'title' :
        apache_analysis.get_title_report(detailed_data_list,data_set)

    if param['report_type'] == 'full' :
        apache_analysis.get_full_report(detailed_data_list,data_set)

    if param['report_type'] == 'all' :
        apache_analysis.get_all_report(detailed_data_list,data_set)
