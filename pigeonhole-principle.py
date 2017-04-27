#!/usr/bin/env python
# coding=utf-8
from collections import defaultdict

def pigeon_hole(hash_set, hash_value):
    hash_value = str(hash_value)

    # 将hash_set之中的每一个元素换成4个dict
    separate = 8
    result_list = []
    for item in hash_set:
        # 先假定每个元素为64位。
        for index in range(0,len(item),separate):
            separate_str = item[index:index + separate]
        
