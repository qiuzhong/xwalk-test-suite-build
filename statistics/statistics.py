#!/usr/bin/env python3

import os
import sys
import json

import xml.etree.ElementTree as ET


platform = {}

def print_test_suite_info(cts_dir, component, test_suite):
    '''
    Print the information of given test suite via the suite.json
    '''
    global platform
    platform[component][test_suite] = {}
    platform[component][test_suite]['android'] = False
    platform[component][test_suite]['windows'] = False
    platform[component][test_suite]['ios'] = False
    platform[component][test_suite]['linux'] = False
    test_suite_root = os.path.join(cts_dir, component, test_suite)
    suite_json_file = os.path.join(test_suite_root, 'suite.json')

    if not os.path.exists(suite_json_file):
        print(test_suite)
        return

    with open(suite_json_file) as fp:
        suite_json = json.load(fp)

    pkg_list = suite_json.get('pkg-list')

    print('*' * 80)
    print(test_suite)
    for k in pkg_list.keys():
        print(k)
        if 'apk' in k or 'cordova' in k or 'embeddignapi' in k:
            platform[component][test_suite]['android'] = True

        if 'msi' in k:
            platform[component][test_suite]['windows'] = True

        if 'ios' in k:
            platform[component][test_suite]['ios'] = True

        if 'deb' in k:
            platform[component][test_suite]['linux'] = True


def print_all_tc_info(json_config_file):

    global platform
    with open(json_config_file) as fp:
        json_data = json.load(fp)

    cts_dir = os.path.expanduser(json_data.get('cts_dir'))
    tcs = json_data.get('test_suite')
    for component in sorted(tcs.keys()):
        platform[component] = {}
        test_suites = tcs.get(component)
        for tc in test_suites:
            print_test_suite_info(cts_dir, component, tc)


def calc_test_suite(cts_dir, component, testsuite, platoforms,
                    use_full_xml = False):
    testcase_statistics = []
    testcase_statistics.append(platforms)
    testcase_statistics.append(component)
    testcase_statistics.append(testsuite)

    if use_full_xml:
        tests_xml_file = 'tests.full.xml'
    else:
        tests_xml_file = 'tests.xml'
    xml_file = os.path.expanduser(os.path.join(cts_dir,
                                            component,
                                            testsuite,
                                            tests_xml_file))
    total_auto = 0
    total_manual = 0

    tests = ET.parse(xml_file)
    xml_root = tests.getroot()
    test_sets = xml_root.findall('suite/set')
    for test_set in test_sets:
        test_cases = test_set.findall('testcase')

        for test_case in test_cases:
            subcase = test_case.get('subcase')
            test_case_type = test_case.get('execution_type')
            if subcase:
                subcase_num = int(subcase)
                if test_case_type == 'auto':
                    total_auto += subcase_num
                elif test_case_type == 'manual':
                    total_manual += subcase_num
                else:
                    print('Unkown test case type!')
            else:
                if test_case_type == 'auto':
                    total_auto += 1
                elif test_case_type == 'manual':
                    total_manual += 1

    total = total_auto + total_manual
    testcase_statistics.append(total_auto)
    testcase_statistics.append(total_manual)
    testcase_statistics.append(total)

    print(testcase_statistics)


def get_test_suite_num(cts_dir, component, test_suite):
    '''
    Get the number of test suite of the given test suite.
    '''
    pass


def check_test_suite(json_config_file):
    with open(json_config_file) as fp:
        json_data = json.load(fp)

    cts_dir = os.path.expanduser(json_data.get('cts_dir'))
    tcs = json_data.get('test_suite')
    tcs = json_data.get('test_suite')
    for component in sorted(tcs.keys()):
        test_suites = tcs.get(component)
        for tc in test_suites:
            abs_tc_dir = os.path.join(cts_dir, component, tc)
            if not os.path.exists(abs_tc_dir):
                print('{tc} does not exists!'.format(tc = tc))
                return False

    return True


class TestSuite:

    CTS_DIR = None

    def __init__(self, component, testsuite):
        self.component = component
        self.testsuite = testsuite

        self.supports_android = False
        self.supports_windows = False
        self.support_linux = False
        self.support_ios = False
        self.is_apptools = False

        self.android_tc_num = None
        self.windows_tc_num = None
        self.linux_tc_num = None
        self.ios_tc_num = None

        self.android_xml = None
        self.windows_xml = None
        self.linux_xml = None
        self.ios_xml = None


    @classmethod
    def set_cts_dir(cls, cts_dir):
        cls.CTS_DIR = os.path.expanduser(cts_dir)


    def check_test_suite(self):
        abs_tc_dir = os.path.join(TestSuite.CTS_DIR,
                                self.component,
                                self.testsuite)
        return os.path.exists(abs_tc_dir)



if __name__ == '__main__':
    json_config_file = __file__.replace('.py', '.json')

    # if check_test_suite(json_config_file):
    #     print('Test suite list is correct!')
    # else:
    #     print('Please check the test suite list first!')

    # print_all_tc_info(json_config_file)
    # print(platform)


    # with open(json_config_file) as fp:
    #     json_data = json.load(fp)
    #
    # cts_dir = json_data.get('cts_dir')
    # component = 'apptools'

    # cts_dir = '~/01_qiuzhong/02-git/crosswalk-project/crosswalk-test-suite'
    # component = 'usecase'
    # testsuite = 'usecase-apptools-tests'
    # platforms = 'all'
    # calc_test_suite(cts_dir, component, testsuite, platforms, True)
