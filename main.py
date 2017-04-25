# -*- coding:utf-8 -*-
# =======================================================
#
# @FileName  : sim_hash.py
# @Author    : Wang Hongqing
# @Date      : 2017-04-24 14:32
#
# =======================================================

import os
import sys
import argparse
import logging
import jieba
import pymongo

#from hashes.simhash import simhash
#from chinese_util import remove_uesless_char
from sim_hashing import SimHash

reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser()
parser.add_argument("--output", help="output file输出")
parser.add_argument("--threshold", help="output file输出")
args = parser.parse_args()

logging.basicConfig(
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%a, %d %b %Y %H:%M:%S'
)

client = pymongo.MongoClient(
    r"mongodb://admin:MzQyZDZjZWQ1Zjg@10.183.99.111:9428/admin")

db = client["galaxy"]
collection = db["content_warehouse"]

result_set = set()
hash_dict = dict()
output_file = open(args.output, "w")
threshold = int(args.threshold)


def process_title(title):
    title = remove_uesless_char(item['title'])
    title_list = [x for x in jieba.cut(title) if x != " "]
    title_cut = " ".join(title_list)
    return title_cut


def get_simhash_object(title):
    hash_result = simhash(title)
    return hash_result


for index, item in enumerate(collection.find()):
    title = item['title']
    new_title = process_title(title)
    hash1 = get_simhash_object(new_title)
    hash_dict[hash1] = title
    for hash2 in result_set:
        distance = hash1.hamming_distance(hash2)
        if distance < threshold:
            output_file.write("%s %s %d" % (hash_dict[hash1], hash_dict[hash2], distance))
            output_file.write("\n")
    result_set.add(hash1)

output_file.close()
