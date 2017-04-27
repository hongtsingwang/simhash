# -*- coding:utf-8 -*-
# =======================================================
#
# @FileName  : repeating_data_process.py
# @Author    : Wang Hongqing
# @Date      : 2017-04-26 10:47
#
# =======================================================

import os
import sys
import argparse
import logging
import datetime
import pymongo
import json
from kafka import KafkaConsumer
from chinese_util import remove_uesless_char

reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser()
parser.add_argument("--output", default=1, help="默认参数")
parser.add_argument("--threshold", type=int, default=6, help="设置的汉明距离的上限")
parser.add_argument("--days_ago", type=int, default=2, help="最早和多少天之前的数据做对比")
args = parser.parse_args()

logging.basicConfig(
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    level=logging.ERROR,
    datefmt='%a, %d %b %Y %H:%M:%S'
)

client = pymongo.MongoClient(
    r"mongodb://admin:MzQyZDZjZWQ1Zjg@10.183.99.111:9428/admin")

db = client["galaxy"]
collection = db["content_warehouse"]

consumer = KafkaConsumer('prod_content', bootstrap_servers=[
                         "10.130.212.117:9092"])

stop_word_file = open("stop_words.utf8")
stop_word_set = set()
for line in stop_word_file:
    line = line.decode('utf-8').strip()
    stop_word_set.add(line)
logging.info("length stop_word_set:%d" % len(stop_word_set))


def process_title(title):
    title = remove_uesless_char(title)
    title_list = [x for x in jieba.cut(
        title) if x != " " and x not in stop_word_set]
    return title_list


def hamming_distance(hash1, hash2, hashbits=64):
    x = (hash1 ^ hash2) & ((1 << hashbits) - 1)
    total = 0
    while x:
        total += 1
        x &= x - 1
    return total


def get_simhash_object(title):
    hash_result = SimHash(title)
    return hash_result


def not_unique(hash_object):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start = (datetime.datetime.now() - datetime.timedelta(1)
             ).strftime("%Y-%m-%d %H:%M:%S")
    result = collection.find("crawl_time": {"$gte": start})
    for item in result:
        item_hash = result['hash']
        distance = hamming_distace(item_hash, hash_object
        if distance <= 6:
            return True
    return False


def process(msg):
    value_dict = json.loads(msg.value)
    status = value_dict['status']
    title = value_dict["title"]
    if int(status) == 1:
        new_title = process_title(title)
        hash_object = get_simhash_object(new_title)
        if not_unique(hash_object)
            collection.update_one({"info_id": info_id}, {
                                  "$set": {"status": 0}})
    return True


def main():
    for msg in consumer:
        is_modified = process(msg)
        if not is_modified:
            logging.error("something must go wrong! stop and call alert!")
            sys.exit(1)


if __name__ == "__main__":
    main()
