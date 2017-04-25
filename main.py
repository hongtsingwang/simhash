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
import datetime

#from hashes.simhash import simhash
from chinese_util import remove_uesless_char
from sim_hashing import SimHash

reload(sys)
sys.setdefaultencoding('utf-8')


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
parser = argparse.ArgumentParser()


def process_title(title):
    title = remove_uesless_char(title)
    title_list = [x for x in jieba.cut(title) if x != " " and x not in stop_word_set]
    return title_list


def get_simhash_object(title):
    hash_result = SimHash(title)
    return hash_result

stop_word_file = open("stop_words.utf8")
stop_word_set = set()
for line in stop_word_file:
    line = line.decode('utf-8').strip()
    stop_word_set.add(line)
logging.info("length stop_word_set:%d" % len(stop_word_set))

def main():
    parser.add_argument("--output", help="output file输出")
    parser.add_argument("--threshold", help="output file输出")
    args = parser.parse_args()
    output_file = open(args.output, "w")
    threshold = int(args.threshold)
    start_date = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d 00:00:00")
    end_date = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d 23:59:59")
    result = collection.find({'crawl_time':{"$gte":start_date,"$lte":end_date}})
    for index, item in enumerate(result):
        title = item['title']
        new_title = process_title(title)
        hash1 = get_simhash_object(new_title)
        hash_dict[hash1] = title
        for hash2 in result_set:
            distance = hash1.hamming_distance(hash2)
            if distance < threshold:
                output_file.write("%s\t%s\t%d" %
                                  (hash_dict[hash1], hash_dict[hash2], distance))
                output_file.write("\n")
        result_set.add(hash1)
    output_file.close()


def test():
    while True:
        #title1 = u"她是身家上亿的豪门千金 却穿借来的衣服路边吃盒饭"
        title1 = raw_input(u"第一句话\n")
        title1 = title1.decode("utf-8")
        new_title1 = process_title(title1)
        for item in new_title1:
            print item
        hash1 = get_simhash_object(new_title1)
        #title2 = u"父亲身家19亿，她穿借来的衣服路边吃盒饭"
        title2 = raw_input(u"第二句话\n")
        title2 = title2.decode("utf-8")
        new_title2 = process_title(title2)
        for item in new_title2:
            print item
        hash2 = get_simhash_object(new_title2)
        distance = hash1.hamming_distance(hash2)
        print "\nresult:%d" % (distance)


if __name__ == "__main__":
    #main()
    test()

