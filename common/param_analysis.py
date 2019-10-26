# -*- coding: utf-8 -*-
import argparse
import re
from tool.log import logger

def check_ip(str):
    '''
    检查ip的合法性
    :param: str:用户输入的ip
    :return:True/False
    '''
    compile_ip = re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}'
                            '|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(str):
        return True
    else:
        return False

def apache_param_analysis():
    '''
    解析用户传进来的参数
    :return:
    {
        'report_type': 'ip',
        'log_file_path': '/sf/log',
        'server_ip': '200.200.1.35',
    }
    '''
    parser = argparse.ArgumentParser()
    parser.description = 'apache-log-analysis'
    
    parser.add_argument('server_ip', help='apache server ip')
    parser.add_argument('log_file_path', help='apache log file path')
    parser.add_argument('report_type', help='report type:article,ip,full,all')
    
    args = parser.parse_args()
    
    # 检查ip的合法性
    if check_ip(args.server_ip):
        logger.info("server_ip is true")
    else:
        logger.info("server_ip is false")
        exit("server_ip is false")

    apache_param = {"server_ip":args.server_ip, "log_file_path":args.log_file_path,
                    "report_type":args.report_type}
    return apache_param

#apache_param_analysis()