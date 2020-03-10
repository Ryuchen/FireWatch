#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2020/3/10-10:29
# @Author : Ryuchen
# @Site : https://ryuchen.github.io
# @File : step_one.py
# @Desc : 
# ==================================================
import os
import glob
import json
import hashlib

_current_dir = os.path.abspath(os.path.dirname(__file__))
DATA_ROOT = os.path.normpath(os.path.join(_current_dir, "..", "data"))
RESULT_ROOT = os.path.normpath(os.path.join(_current_dir, "..", "result"))

title = ['mid', '作者ID', '发布日期', '地址', '地域', '城市', '性别', '标题／微博内容', '粉丝数', '认证类型', '评', '赞', '转']


def get_md5(s):
    md = hashlib.md5()
    md.update(s.encode('utf-8'))
    return md.hexdigest()


def get_content(data):
    """
    我们把数据中的标题/微博内容抽取出来，然后将其他的数据作为metadata补充
    我们赋予metadata一个id这个id与抽取出来的内容进行关联，减少后续处理时的数据量
    """
    with open(os.path.join(RESULT_ROOT, "meta.csv"), "a+") as meta_obj:
        meta_obj.write("{0}\n".format("uid, mid, 作者ID, 发布日期, 地址, 地域, 城市, 性别, 粉丝数, 认证类型, 评, 赞, 转"))
        with open(os.path.join(RESULT_ROOT, "content.csv"), "a+") as content_obj:
            with open(data, "r") as raw:
                line = raw.readline()
                while line:
                    columns = line.rstrip("\n").split(",")
                    dictionary = dict(zip(title, columns))
                    uid = get_md5(json.dumps(dictionary))
                    metadata = {"uid": uid}
                    metadata.update(dictionary)
                    del metadata['标题／微博内容']
                    meta = metadata["uid"] + ", "
                    meta += metadata["mid"] + ", "
                    meta += metadata["作者ID"] + ", "
                    meta += metadata["发布日期"] + ", "
                    meta += metadata["地址"] + ", "
                    meta += metadata["地域"] + ", "
                    meta += metadata["城市"] + ", "
                    meta += metadata["性别"] + ", "
                    meta += metadata["粉丝数"] + ", "
                    meta += metadata["认证类型"] + ", "
                    meta += metadata["评"] + ", "
                    meta += metadata["赞"] + ", "
                    meta += metadata["转"]
                    meta_obj.write('{0}\n'.format(meta))
                    content_obj.write('{0}\n'.format({"uid": uid, "text": dictionary['标题／微博内容']}))
                    line = raw.readline()


if __name__ == '__main__':
    if os.path.exists(os.path.join(RESULT_ROOT, "meta.csv")):
        os.remove(os.path.join(RESULT_ROOT, "meta.csv"))
    if os.path.exists(os.path.join(RESULT_ROOT, "content.csv")):
        os.remove(os.path.join(RESULT_ROOT, "content.csv"))
    data_sets = glob.glob(os.path.join(DATA_ROOT, 'part_*.csv'))
    for item in data_sets:
        print(item)
        get_content(item)

