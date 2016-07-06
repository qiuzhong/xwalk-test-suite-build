#!/usr/bin/env python3


import os
import json


class TestSuite:

    CTS_DIR = None

    def __init__(self, component, testsuite):
        self.component = component
        self.testsuite = testsuite

        self.supports_android = False
        self.supports_windows = False
        self.support_linux = False
        self.support_ios = False
        self.support_cordova = False
        self.support_aio = False

        self.is_apptools = False

        self.android_tc_num = None
        self.windows_tc_num = None
        self.linux_tc_num = None
        self.ios_tc_num = None

        self.android_xml = None
        self.windows_xml = None
        self.linux_xml = None
        self.ios_xml = None

        self.abs_tc_dir = None
        self.abs_suite_json = None


    @classmethod
    def set_cts_dir(cls, cts_dir):
        cls.CTS_DIR = os.path.expanduser(cts_dir)


    def check_test_suite(self):
        self.abs_tc_dir = os.path.join(TestSuite.CTS_DIR,
                                self.component,
                                self.testsuite)

        return os.path.exists(self.abs_tc_dir)


    def check_is_apptools(self):
        if self.component == 'apptools':
            return True

        if self.testsuite == 'usecase-apptools-tests':
            return True

        return False


    def check_test_suite_json(self):
        if not self.check_test_suite():
            return False
        self.abs_suite_json = os.path.join(self.abs_tc_dir,
                                            'suite.json')

        return os.path.exists(self.abs_suite_json)


    def read_suite_json(self):
        with open(suite_json_file) as fp:
            suite_json = json.load(fp)

        pkg_list = suite_json.get('pkg-list')
        for package_type in pkg_list.keys():
            if 'apk' == package_type:
                self.supports_android = True
                self.android_xml = pkg_list.get(package_type).get(
                                                'copylist').get(
                                                'tests.android.xml'
                                                )
                if not self.android_xml:
                    self.android_xml = 'tests.xml'

            if 'cordova' in pack_type:
                self.supports_android = True
                self.support_cordova = True
                self.android_xml = pkg_list.get(package_type).get(
                                                'copylist').get(
                                                'tests.android.xml'
                                                )
                if not self.android_xml:
                    self.android_xml = 'tests.xml'

            if 'apk-aio' in package_type:
                self.supports_android = True
                self.support_ios = True
                self.android_xml = pkg_list.get(package_type).get(
                                                'copylist').get(
                                                'tests.android.xml'
                                                )
                if not self.android_xml:
                    self.android_xml = 'tests.xml'

            if 'cordova-aio' in package_type:
                self.supports_android = True
                self.support_cordova = True
                self.support_aio = True
                self.android_xml = pkg_list.get(package_type).get(
                                                'copylist').get(
                                                'tests.android.xml'
                                                )
                if not self.android_xml:
                    self.android_xml = 'tests.xml'

            if 'msi' in package_type:
                self.support_windows = True
                self.android_xml = pkg_list.get(package_type).get(
                                                'copylist').get(
                                                'tests.windows.xml'
                                                )
                if not self.android_xml:
                    self.android_xml = 'tests.xml'

            if 'deb' in package_type:
                self.support_linux = True

            if 'ios' in pack_type:
                self.support_ios = True
