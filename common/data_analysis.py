import re
import data_load

class ApacheAnalysis(object):
    def get_ip_url(self, data):
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

    def get_detailed_data(self,log_file_data):
        detailed_data_list = []
        for data in log_file_data:
            data_info = self.get_ip_url(data)
            if data is not None:
                #print(data)
                detailed_data_list.append(data_info)
        return detailed_data_list

    def get_ip_report(self, detailed_data_list):
        ip_set = set([])
        for data in detailed_data_list:
            if data:
                ip_set.add(data['ip'])
                #print(ip_set)
        for ip in ip_set:
            visit_count = 0
            for data in detailed_data_list:
                if data is not None:
                    if ip is data['ip']:
                        print("ss")
                        visit_count = visit_count+1
                        if data['url']:
                            print(visit_count)
            print(visit_count)

test_data_base = data_load.DataBase()
log_file_data = test_data_base.read_log_file("C:/Users/lis/Desktop/丰羽计划/apache日志分析/apache.log")
test_apache_analysis = ApacheAnalysis()
detailed_data_list = test_apache_analysis.get_detailed_data(log_file_data)
#print(detailed_data_list)
test_apache_analysis.get_ip_report(detailed_data_list)