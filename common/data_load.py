#import urllib2
import re
class DataBase(object):
    def read_log_file(self, log_file_path):
        log_file = open(log_file_path, 'r')
        log_file_data = log_file.read()
        log_list_data = log_file_data.split('\n')
        log_file.close()
        return log_list_data

#test_data_base = DataBase()
#log_file_data = test_data_base.read_log_file("C:/Users/lis/Desktop/丰羽计划/apache日志分析/apache.log")
#test_data_base.get_ip_report(log_file_data)