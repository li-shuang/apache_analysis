# -*- coding: utf-8 -*-
from tool.log import logger

class DataBase(object):
    def read_log_file(self, log_file_path):
        """
        将log文件中的日志信息读取，并处理成列表的形式
        :param log_file_path:log文件的路径
        :return:[
                    '200.200.76.130--[16/Feb/2019: 11: 27: 20+0800]"GET /coding/miniprj/material.html HTTP/1.1"20038093',
                    '200.200.76.130--[16/Feb/2019: 11: 27: 20+0800]"GET /coding/gitbook/gitbook-plugin-search-plus/search.css HTTP/1.1"2001095',
                    '200.200.76.130--[16/Feb/2019: 11: 27: 20+0800]"GET /coding/gitbook/gitbook-plugin-disqus/plugin.css HTTP/1.1"20063',
                    '200.200.76.130--[16/Feb/2019: 11: 27: 20+0800]"GET /coding/gitbook/gitbook-plugin-prism/prism-base16-ateliersulphurpool.light.css HTTP/1.1"2003290'

                ]
        """
        try:
            log_file = open(log_file_path, 'r')
        except Exception as ex:
            logger.warning("read %(log_file_path)s is error. %(err)s"
                            % {'log_file_path': log_file_path, 'err': ex})
            raise Exception('Read log file failed')

        log_file_data = log_file.read()
        log_list_data = log_file_data.split('\n')
        log_file.close()
        return log_list_data


#test_data_base = DataBase()
#html = test_data_base.get_url_html("http://200.200.1.35/coding/miniprj/material.html")
#print(test_data_base.read_log_file("/home/ls/log.txt"))