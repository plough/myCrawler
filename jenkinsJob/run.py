#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 关键配置脱敏，不能直接运行。如要使用，需自行调试
from selenium import webdriver
import time
from utils import LogInfo


USER_NAME = 'yourname'
PASSWD = 'yourpassword'
HOST = 'https://ci.xxx.com/jenkins'

browser = webdriver.Chrome()


def main():
    login(browser)
    job_list = ['yourjob']
    for job in job_list:
        fetch_build_info(job)


def fetch_build_info(job):
    result_map = init_result_map(job)
    for build_number in result_map.keys():
        info_map = result_map[build_number]
        blue_url = get_blue_url(job, build_number)
        browser.get(blue_url)
        time.sleep(5)
        info_map['msg'] = browser.find_element_by_css_selector(
            'div.causes').text
        if info_map['status'] == 'failed':
            try:
                fail_step = browser.find_element_by_css_selector(
                    'div.TruncatingLabel.PWGx-pipeline-big-label.selected'
                ).text
                info_map['fail_step'] = fail_step
            except Exception as e:
                print(e)
                info_map['fail_step'] = 'init'
        log_consoles = browser.find_elements_by_css_selector('div.logConsole')
        if len(log_consoles) > 0:
            log_consoles[-1].click()
            time.sleep(3)
        log_body = browser.find_elements_by_css_selector(
            'div.log-body')[-1].text
        log_info = LogInfo(log_body)
        info_map['end_time'] = log_info.get_end_time()
        info_map['end_time_str'] = log_info.get_end_time_str()
        info_map['ci_ip'] = log_info.get_ci_ip()
        info_map['paas_ip'] = log_info.get_paas_ip()
    print(result_map)


def get_blue_url(job, build_number):
    return '{0}/blue/organizations/jenkins/{1}/detail/{1}/{2}/pipeline'\
        .format(HOST, job, build_number)


def get_trend_url(job):
    return '{0}/view/OPOD/job/{1}/buildTimeTrend'.format(HOST, job)


def init_result_map(job):
    result_map = {}
    trend_url = get_trend_url(job)
    browser.get(trend_url)
    time.sleep(5)
    table = browser.find_element_by_id('trend')
    # rows = table.find_elements_by_tag_name('tr')[1:]
    rows = table.find_elements_by_tag_name('tr')[1:20]
    for row in rows:
        tds = row.find_elements_by_tag_name('td')
        # 忽略进行中的任务
        status = translate_status(tds[0].get_attribute('data'))
        if status == '-1':
            continue
        number = tds[1].get_attribute('data')
        duration_ms = tds[2].get_attribute('data')
        duration_text = tds[2].text
        result_map[number] = {
            'status': status,
            'duration_ms': duration_ms,
            'duration_text': duration_text
        }
    return result_map


def translate_status(old_status):
    """
    -1: 进行中
    """
    trans_map = {
        '1': '-1',
        '0': 'failed',
        '4': 'success',
        '10': 'aborted'
    }
    assert old_status in trans_map.keys()
    return trans_map[old_status]


def login(browser):
    browser.get('https://ci.xxx.com/jenkins/login')
    username_field = browser.find_element_by_name('j_username')
    username_field.send_keys(USER_NAME)
    passwd_field = browser.find_element_by_name('j_password')
    passwd_field.send_keys(PASSWD)
    login_btn = browser.find_element_by_name('Submit')
    login_btn.click()


if __name__ == "__main__":
    main()
