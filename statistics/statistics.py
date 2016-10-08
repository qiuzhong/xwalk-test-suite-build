#!/usr/bin/env python3

import os
import sys
import json
import glob
import collections
import argparse

import xml.etree.ElementTree as ET


platform = {}
PWD = os.getcwd()

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


def print_tc_package_type(json_config_file, component):
    with open(json_config_file) as fp:
        json_data = json.load(fp)

    tc_num = 0
    cts_dir = os.path.expanduser(json_data.get('cts_dir'))
    testsuites = json_data.get('test_suite').get(component)
    for tc, _ in sorted(testsuites.items(), key = lambda l: l[0]):
        print(tc, end = ':')
        suite_json_file = os.path.join(cts_dir, tc, "suite.json")

        if not os.path.exists(suite_json_file):
            print('test_suite does not exist!')
            return
        with open(suite_json_file) as fp:
            suite_json = json.load(fp)

        pkg_list = suite_json.get('pkg-list')
        for k in sorted(pkg_list.keys()):
            print(k, end = ';')

        os.chdir(os.path.join(cts_dir, tc))
        xml_files = glob.glob('*.xml')
        print(xml_files, end = '.\n')
        tc_num += 1

    print(tc_num)


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


def print_apptools_tc_info(json_config_file):
    '''
    Print the number of test suite in apptools component.
    '''
    with open(json_config_file) as fp:
        json_data = json.load(fp)

    cts_dir = os.path.expanduser(json_data.get('cts_dir'))
    testsuites = json_data.get('test_suite').get('apptools')
    for app_tools_tc, platform_xml in testsuites.items():
        # print(app_tools_tc)
        testcase_info = []
        testcase_info.append('apptools')
        testcase_info.append(app_tools_tc.split('/')[-1])

        tests_xml = os.path.expanduser(os.path.join(cts_dir,
                                                    app_tools_tc,
                                                    "tests.full.xml"))
        testcase_info += parse_tests_xml(tests_xml)
        print(testcase_info)


def print_tc_info(json_config_file, component, platform = 'android'):
    '''
    Print the number of test suite in apptools component.
    '''
    global PWD
    os.chdir(PWD)
    with open(json_config_file) as fp:
        json_data = json.load(fp)

    total_all = 0
    total_auto = 0
    total_manual = 0

    cts_dir = os.path.expanduser(json_data.get('cts_dir'))
    testsuites = json_data.get('test_suite').get(component)
    testcase_info_all = []
    for webapi_tc, platform_xmls in sorted(testsuites.items(), key = lambda l: l[0]):
        testcase_info = []
        testcase_info.append(component)
        testcase_info.append(webapi_tc.split('/')[-1])

        test_xml = platform_xmls.get(platform)
        if test_xml:
            abs_tests_xml = os.path.expanduser(os.path.join(cts_dir,
                                                    webapi_tc,
                                                    test_xml))
            testcase_info.append(parse_tests_xml(abs_tests_xml))

            testcase_info_all.append(testcase_info)

    # print(testcase_info_all)

    all_line = []
    all_line.append(component)
    all_line.append('All')
    for tc_info in testcase_info_all:
        print(tc_info)
        total_all += tc_info[2][0]
        total_auto += tc_info[2][1]
        total_manual += tc_info[2][2]

    all_line.append(total_all)
    all_line.append(total_auto)
    all_line.append(total_manual)
    print('*' * 80)
    print(all_line)


def parse_tests_xml(xml_file):

    testcase_statistics = []
    total_auto = 0
    total_manual = 0

    tests = ET.parse(xml_file)
    xml_root = tests.getroot()
    test_sets = xml_root.findall('suite/set')
    for test_set in test_sets:
        test_cases = test_set.findall('testcase')

        for test_case in test_cases:
            line = []
            case_id = test_case.get('id')
            line.append(case_id)
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

                line.append(subcase_num)
            else:
                if test_case_type == 'auto':
                    total_auto += 1
                elif test_case_type == 'manual':
                    total_manual += 1
                line.append(1)

    total = total_auto + total_manual
    testcase_statistics.append(total)
    testcase_statistics.append(total_auto)
    testcase_statistics.append(total_manual)
    
    return testcase_statistics



def calc_test_suite(cts_dir, component, testsuite, platoforms,
                    use_full_xml = False):
    testcase_statistics = []
    testcase_statistics.append(platforms)
    testcase_statistics.append(component)
    testcase_statistics.append(testsuite)

    if use_full_xml:
        tests_xml_file = 'tests.full.xml'
    else:
        tests_xml_file = 'tests_v7.xml'
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
            line = []
            case_id = test_case.get('id')
            line.append(case_id)
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

                line.append(subcase_num)
            else:
                if test_case_type == 'auto':
                    total_auto += 1
                elif test_case_type == 'manual':
                    total_manual += 1
                line.append(1)

            print(line)


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
    for component in sorted(tcs.keys()):
        test_suites = tcs.get(component)
        for tc in test_suites:
            abs_tc_dir = os.path.join(cts_dir, component, tc)
            if not os.path.exists(abs_tc_dir):
                print('{tc} does not exists!'.format(tc = tc))
                return False

    return True


if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description = 'Get the test case number information.')


    json_config_file = 'testsuites.json'
    # print_tc_package_type(json_config_file, 'webapi')
    print('*' * 80)
    print_tc_info(json_config_file, 'usecase', 'windows')
