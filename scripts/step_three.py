#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2020/3/10-15:44
# @Author : Ryuchen
# @Site : https://ryuchen.github.io
# @File : step_three.py
# @Desc : 
# ==================================================
import os
import re
import sys
import hashlib

_current_dir = os.path.abspath(os.path.dirname(__file__))
DATA_ROOT = os.path.normpath(os.path.join(_current_dir, "..", "data"))
RESULT_ROOT = os.path.normpath(os.path.join(_current_dir, "..", "result"))

context_md5s = set()
sentence_md5s = set()

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


def get_md5(s):
    md = hashlib.md5()
    md.update(s.encode('utf-8'))
    return md.hexdigest()


def split_content():
    with open(os.path.join(RESULT_ROOT, "sentences.csv"), "a+") as sentence_obj:
        with open(os.path.join(RESULT_ROOT, "articles.csv"), "a+") as article_obj:
            with open(os.path.join(RESULT_ROOT, "meta.csv"), "r") as meta_obj:
                with open(os.path.join(RESULT_ROOT, "content.csv"), "r") as content_obj:
                    title = meta_obj.readline().rstrip("\n").split(", ")
                    meta_line = meta_obj.readline().rstrip("\n")
                    content_line = content_obj.readline().rstrip("\n")
                    while meta_line and content_line:
                        columns = meta_line.rstrip("\n").split(", ")
                        if "null" in columns[1]:
                            metadata = dict(zip(title, columns))
                            article_obj.write("{0}\n".format(metadata))
                            article_obj.write("{0}\n".format(content_line))
                        else:
                            # 只提取text的部分，因为是str格式，所以只能用截取的方法
                            context = content_line[53:-2]
                            context_md5 = get_md5(context)
                            if context_md5 not in context_md5s:
                                # 过滤用户名称是关键字的情况
                                if any("@{0}".format(keyword) in context for keyword in keywords):
                                    pass
                                else:
                                    # 删除内容末尾的 ‘ ??’
                                    context = context.strip(' ??')
                                    # 只存储包含关键字的文本内容
                                    if any("{0}".format(keyword) in context for keyword in keywords):
                                        sentences = re.split('~|。', context)
                                        # 去除相同文本内容中的相同的句子
                                        for sentence in sentences:
                                            sentence = sentence.strip()
                                            sentence_md5 = get_md5(sentence)
                                            if sentence_md5 not in sentence_md5s:
                                                # 去除掉目标句子中的'??' TODO：未知标识符
                                                sentence = sentence.replace('??', '')
                                                # 句子长度小于 3 个字符的不会包含有效信息
                                                if len(sentence) > 3:
                                                    # 去除掉微博特定的话题标识符
                                                    sentence = re.sub('【.*】', '', sentence)
                                                    # 去除掉url内容
                                                    sentence = re.sub(
                                                        "(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\[a-zA-Z0-9\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*",
                                                        '',
                                                        sentence
                                                    )
                                                    sentence_obj.write("{0}\n".format(sentence))
                                                    sentence_md5s.add(sentence_md5)
                                context_md5s.add(context_md5)
                        meta_line = meta_obj.readline().rstrip("\n")
                        content_line = content_obj.readline().rstrip("\n")


if __name__ == '__main__':
    if not os.path.exists(os.path.join(RESULT_ROOT, "meta.csv")):
        print("please run step_one.py scripts first.")
        sys.exit(1)

    if not os.path.exists(os.path.join(RESULT_ROOT, "content.csv")):
        print("please run step_one.py scripts first.")
        sys.exit(1)

    if os.path.exists(os.path.join(RESULT_ROOT, "sentences.csv")):
        os.remove(os.path.join(RESULT_ROOT, "sentences.csv"))

    if os.path.exists(os.path.join(RESULT_ROOT, "articles.csv")):
        os.remove(os.path.join(RESULT_ROOT, "articles.csv"))

    # if os.path.exists(os.path.join(RESULT_ROOT, "properties.csv")):
    #     os.remove(os.path.join(RESULT_ROOT, "properties.csv"))

    split_content()
