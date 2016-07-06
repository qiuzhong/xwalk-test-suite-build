#!/usr/bin/env python3

import xml.etree.ElementTree as ET

tests_file = '/home/orange/01_qiuzhong/02-git/crosswalk-project/crosswalk-test-suite/apptools/apptools-android-tests/tests.xml'
data = ET.parse(tests_file)
