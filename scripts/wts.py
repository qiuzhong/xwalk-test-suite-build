#!/usr/bin/env python3


sum_num = 0
manaul_num = 0
other_num = 0

with open('wts.txt') as f:
    for line in f:
        info = line.strip().split(';')
        tc_num = int(info[0])
        sum_num += tc_num
        manaul_num += int(info[1])
        other_num += int(info[2])

print('all summary:', sum_num) 
print('manaul:', manaul_num)
print('other:', other_num)       