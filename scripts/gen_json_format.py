#!/usr/bin/env python3


import json


s = '''
webapi-noneservice-tests
webapi-service-docroot-tests
webapi-service-tests
'''

lines = s.strip().split('\n')
json_line_str = ',\n'.join(['"' + line + '"' for line in lines])
print(json_line_str)
