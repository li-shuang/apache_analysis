import argparse
import re

def check_ip(str):
    compile_ip = re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}'
                            '|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(str):
        return True
    else:
        return False

def apache_param_analysis():
    u"""
    解析用户输入的参数
    :return:
    {
	    'report_type': 'ip',
	    'log_file_path': '/sf/log',
	    'server_ip': '200.200.1.35',
	    'analysis_file_save_path': '/sf/lishuang'
    }
    """
    parser = argparse.ArgumentParser()
    parser.description = 'apache-log-analysis'
    parser.add_argument('server_ip', help='apache server ip')
    parser.add_argument('log_file_path', help='apache log file path')
    parser.add_argument('report_type', help='report type:article,ip,full,all')
    parser.add_argument('analysis_file_save_path', help='report file save path')
    args = parser.parse_args()
    if check_ip(args.server_ip):
        print("server_ip is true")
    else:
        exit("server_ip is false")
    apache_param = {"server_ip":args.server_ip, "log_file_path":args.log_file_path,
                    "report_type":args.report_type, "analysis_file_save_path":args.analysis_file_save_path}
    print(apache_param)
    return apache_param

apache_param_analysis()