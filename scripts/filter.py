#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2020/3/9-13:42
# @Author : Ryuchen
# @Site : https://ryuchen.github.io
# @File : filter.py
# @Desc : 
# ==================================================
import os
import re
import hanlp

title = ['mid', '作者ID', '发布日期', '地址', '地域', '城市', '性别', '标题／微博内容', '粉丝数', '认证类型', '评', '赞', '转']

keywords = [
    "蒜你狠", "豆你玩", "姜你军", "糖高宗", "苹什么", "药你命", "苹天下", "苹什么", "苹跳跳", "棉里针", "煤超疯", "贵金属", "重金属",
    "有色金属", "原油", "农产品", "大宗商品", "现货交易", "期货交易", "港口大宗交易市场", "应收账款融资", "保兑仓融资", "仓单质押融资",
    "铜", "铝", "锌", "铅", "镍", "锡", "黄", "金", "白", "银",
    "螺纹钢", "线材", "冷轧钢板", "不锈钢", "上涨", "下跌", "波动", "价格", "民生", "终端价格",
    "蒜你狠", "豆你玩", "姜你军", "糖高宗", "苹什么", "药你命", "苹天下", "苹什么", "苹跳跳", "棉里针", "煤超疯",
    "大蒜", "大葱", "猪肉", "羊肉", "牛肉", "羊绒", "棉籽", "棉短绒", "夏枯草", "黄连", "半枝莲", "枸杞", "金银花",
    "红参", "柞蚕茧壳", "梅花鹿鹿", "肉苁蓉", "白参", "太子参", "黑芝麻", "花生仁", "香菇", "白芝麻", "葛根",
    "沪镍", "红枣", "沪铝", "棉纱", "石油沥青", "棉花", "新甲醇", "白银", "沪铜", "沪铅", "鸡蛋", "菜籽粕", "豆粕", "晚籼稻", "燃料油", "黄金",
    "纤维板", "玻璃", "粳米", "强麦", "新动力煤", "铁矿石", "乙二醇", "聚乙烯", "玉米", "菜籽油", "焦煤", "白糖",
    "玉米淀粉", "尿素", "焦炭", "豆一", "PTA", "聚丙烯", "沪锌", "聚氯乙烯", "苹果", "硅铁", "豆二", "天胶", "螺纹钢",
    "热轧卷板", "棕榈油", "豆油", "纸浆", "锰硅", "沪锡", "普麦", "胶合板", "晚籼稻", "东证",
    "大商所农产品指数", "猪饲料成本指数", "铁矿石期货价格指数", "农产品期货 价格指数", "油脂油料期货价格指数", "大豆类期货价格指数", "饲料类期货价格指数",
    "豆粕期货价格指数", "农产品期货价格综合指数", "工业品期货价格指数", "黑色系期货价格指数", "化工期货价格指数", "工业品期货价格综合指数", "玉米期货近月合约价格指数",
    "玉米淀粉期货近月合约价格指数", "豆油期货近月合约价格指数", "棕榈油期货近月合约价格指数", "豆粕期货近月合约价格指数", "豆一期货近月合约价格指数",
    "聚丙烯期货近月合约价格指数", "聚氯乙烯期货近月合约价格指数", "聚乙烯期货近月合约价格指数", "焦煤期货近月合约价格指数", "焦炭期货近月合约价格指数",
    "铁矿石期货近月合约价格指数", "鸡蛋期货近月合约价格指数", "聚乙烯期货价格指数", "聚氯乙烯期货价格指数", "聚丙烯期货价格指数", "豆一期货价格指数",
    "棕榈油期货价格指数", "豆油期货价格指数", "玉米淀粉期货价格指数", "玉米期货价格指数", "鸡蛋期货价格指数", "铁矿石期货主力合约价格指数", "焦炭期货主力合约价格指数"
]


def get_content():
    contents = []
    with open(os.path.join(os.curdir, "data", "part_1.csv"), "r") as raw:
        line = raw.readline()
        while line:
            columns = line.split(",")
            if "T" in columns[-1]:
                contents.append(columns[7])
            line = raw.readline()

    with open(os.path.join(os.curdir, "result", "content.txt"), "w") as valid:
        for content in contents:
            valid.write("{}\n".format(content))


def spilt_sentence():
    sentences = []
    with open(os.path.join(os.curdir, "result", "content.txt"), "r") as raw:
        line = raw.readline()
        while line:
            if any(keyword in line for keyword in keywords):
                sentences.extend(re.split('~|。', line))
            line = raw.readline()

    with open(os.path.join(os.curdir, "result", "sentence.txt"), "w") as valid:
        for sentence in sentences:
            valid.write("{}\n".format(sentence.replace(" ", "")))


if __name__ == '__main__':
    # get_content()
    # spilt_sentence()
    # tokens = set()
    # tokenizer = hanlp.load('PKU_NAME_MERGED_SIX_MONTHS_CONVSEG')
    # with open(os.path.join(os.curdir, "result", "sentence.txt"), "r") as target:
    #     lines = target.readlines()
    #     for line in lines:
    #         if line:
    #             tokens = tokenizer(line)
    #             print(tokens)
    with open(os.path.join(os.curdir, "data", "part_1.csv"), "r") as raw:
        line = raw.readlines()
        titles = line[0].rstrip("\n")
        row1 = line[1].rstrip("\n")
        keys = titles.split(",")
        print(keys)
        values = row1.split(",")
        dictionary = dict(zip(keys, values))
        print(dictionary)
