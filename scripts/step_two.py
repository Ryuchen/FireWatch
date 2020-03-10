#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================
# @Time : 2020/3/10-14:18
# @Author : Ryuchen
# @Site : https://ryuchen.github.io
# @File : step_two.py
# @Desc : 
# ==================================================
import os
import sys

_current_dir = os.path.abspath(os.path.dirname(__file__))
DATA_ROOT = os.path.normpath(os.path.join(_current_dir, "..", "data"))
RESULT_ROOT = os.path.normpath(os.path.join(_current_dir, "..", "result"))

entity_one = ['mid']
entity_two = ['作者ID']
entity_three = ['地域']
entity_four = ['城市']

entities_one = set()
entities_two = set()
entities_three = set()
entities_four = set()


def split_entity():
    entity_start_with = 10000

    with open(os.path.join(RESULT_ROOT, "entity.csv"), "a+") as entity_obj:
        entity_obj.write(":ID, name, :LABEL\n")
        with open(os.path.join(RESULT_ROOT, "relation.csv"), "a+") as relation_obj:
            relation_obj.write(":START_ID, name, :END_ID, :TYPE\n")
            with open(os.path.join(RESULT_ROOT, "properties.csv"), "a+") as property_obj:
                property_obj.write(":ENTITY_ID, prop_name, prop_value\n")
                with open(os.path.join(RESULT_ROOT, "meta.csv"), "r") as meta_obj:
                    print("Title: {0}".format(meta_obj.readline().rstrip("\n")))
                    line = meta_obj.readline()
                    while line:
                        columns = line.rstrip("\n").split(", ")
                        mid_entity_id = ""
                        author_entity_id = ""
                        province_entity_id = ""
                        city_entity_id = ""
                        # ---------------- 生成实体 ---------------- #
                        # 生成 mid 的 Node
                        if columns[1].strip():
                            if "null" not in columns[1] and columns[1] not in entities_one:
                                mid_entity_id = "MID{0}".format(entity_start_with)
                                entity_obj.write("{0}, {1}, {2}\n".format(mid_entity_id, columns[1], "MID"))
                                entities_one.add(columns[1])
                                entity_start_with += 1
                        # 生成 作者ID 的 Node
                        if columns[2].strip():
                            if "null" not in columns[2] and columns[2] not in entities_one:
                                author_entity_id = "AUTH{0}".format(entity_start_with)
                                entity_obj.write("{0}, {1}, {2}\n".format(author_entity_id, columns[2], "AUTH"))
                                entities_two.add(columns[2])
                                entity_start_with += 1
                        # 生成 地域 的 Node
                        if columns[5].strip():
                            if "null" not in columns[5] and columns[5] not in entities_one:
                                province_entity_id = "PROV{0}".format(entity_start_with)
                                entity_obj.write("{0}, {1}, {2}\n".format(province_entity_id, columns[5], "PROV"))
                                entities_three.add(columns[5])
                                entity_start_with += 1
                        # 生成 城市 的 Node
                        if columns[6].strip():
                            if "null" not in columns[6] and columns[6] not in entities_one:
                                city_entity_id = "CITY{0}".format(entity_start_with)
                                entity_obj.write("{0}, {1}, {2}\n".format(city_entity_id, columns[6], "CITY"))
                                entities_four.add(columns[6])
                                entity_start_with += 1

                        # ---------------- 生成关系 ---------------- #
                        if mid_entity_id and author_entity_id:
                            relation_obj.write("{0}, {1}, {2}, {3}\n".format(
                                mid_entity_id, "is published by", author_entity_id, "RELATIONSHIP"
                            ))
                        if author_entity_id and province_entity_id:
                            relation_obj.write("{0}, {1}, {2}, {3}\n".format(
                                author_entity_id, "is locate at", province_entity_id, "RELATIONSHIP"
                            ))
                        if province_entity_id and city_entity_id:
                            relation_obj.write("{0}, {1}, {2}, {3}\n".format(
                                city_entity_id, "is part of", province_entity_id, "RELATIONSHIP"
                            ))

                        # ---------------- 生成属性 ---------------- #
                        if mid_entity_id:
                            property_obj.write("{0}, {1}, {2}\n".format(mid_entity_id, "published_date", columns[3]))
                            property_obj.write("{0}, {1}, {2}\n".format(mid_entity_id, "post_url", columns[4]))
                            property_obj.write("{0}, {1}, {2}\n".format(mid_entity_id, "comment_num", columns[10]))
                            property_obj.write("{0}, {1}, {2}\n".format(mid_entity_id, "like_num", columns[11]))
                            property_obj.write("{0}, {1}, {2}\n".format(mid_entity_id, "share_num", columns[12]))
                        if author_entity_id:
                            property_obj.write("{0}, {1}, {2}\n".format(author_entity_id, "sex", columns[7]))
                            property_obj.write("{0}, {1}, {2}\n".format(author_entity_id, "fans_num", columns[8]))
                            property_obj.write("{0}, {1}, {2}\n".format(author_entity_id, "auth_type", columns[9]))

                        line = meta_obj.readline()


if __name__ == '__main__':
    if not os.path.exists(os.path.join(RESULT_ROOT, "meta.csv")):
        print("please run step_one.py scripts first.")
        sys.exit(1)

    if os.path.exists(os.path.join(RESULT_ROOT, "entity.csv")):
        os.remove(os.path.join(RESULT_ROOT, "entity.csv"))

    if os.path.exists(os.path.join(RESULT_ROOT, "relation.csv")):
        os.remove(os.path.join(RESULT_ROOT, "relation.csv"))

    if os.path.exists(os.path.join(RESULT_ROOT, "properties.csv")):
        os.remove(os.path.join(RESULT_ROOT, "properties.csv"))

    split_entity()
