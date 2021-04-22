#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import re


class LogInfo:
    """
    从一串日志文本中，提取以下信息：
        1. 运行时间的 timestamp（单位s）
        2. ci 机器的 ip
        3. paas 机器的 ip
    """
    CI_IP_PREFIX = 'run on ip:'
    PAAS_IP_PREFIX = 'PAAS ip:'

    def __init__(self, text):
        last_line = text.split('\n')[-2]
        self.end_time_str = last_line.split(' ')[0].strip('[]')[:-5]
        end_time = time.strptime(self.end_time_str, '%Y-%m-%dT%H:%M:%S')
        self.end_time = int(time.mktime(end_time))
        self.ci_ip = ''
        self.paas_ip = ''
        if LogInfo.CI_IP_PREFIX in text:
            self.ci_ip = re.findall(
                r'{} (.+?)\n'.format(LogInfo.CI_IP_PREFIX), text)[0]
        if LogInfo.PAAS_IP_PREFIX in text:
            self.paas_ip = re.findall(
                r'{} (.+?)\n'.format(LogInfo.PAAS_IP_PREFIX), text)[0]

    def __str__(self):
        return 'end time: {}  ci ip: {}  paas ip: {}'.format(
            self.get_end_time_str(),
            self.get_ci_ip(),
            self.get_paas_ip()
        )

    def get_end_time(self):
        return self.end_time

    def get_end_time_str(self):
        return self.end_time_str

    def get_ci_ip(self):
        return self.ci_ip

    def get_paas_ip(self):
        return self.paas_ip


if __name__ == "__main__":
    s = '[2020-02-28T12:20:31.285Z] + pwd\n[2020-02-28T12:20:31.285Z] /home/jenkins/ci/ficus2/merge_request/product/opod\n[2020-02-28T12:20:31.285Z] + bash ./tool/ci/utils/print_debug_info.sh\n[2020-02-28T12:20:31.285Z] #################\n[2020-02-28T12:20:31.285Z] Running Env Info\n[2020-02-28T12:20:31.285Z] #################\n[2020-02-28T12:20:31.285Z] run on ip: 10.40.50.73\n[2020-02-28T12:20:31.285Z] PAAS ip: 10.40.52.111\n[2020-02-28T12:20:31.285Z] See backup log files in ~/opod_logs/ on PAAS machine.'
    log_info = LogInfo(s)
    print(log_info)
