#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: dj
@contact: dj@itmojun.com
@software: PyCharm
@file: main.py
@time: 2018/11/1 14:05
"""

import re
import requests

def main():
    while True:
        cardno = input("\n请输入身份证号：")

        # 调用本地函数实现
        r = get_idcard_info(cardno)

        # 调用接口实现
        # r = requests.get("http://api.itmojun.com/idcard", params={"cardno": cardno})
        # r = r.json()

        if r["err"]:
            print("输入错误，请重新输入！")
        else:
            print("地址：%s\n生日：%s\n性别：%s" % (r["area"], r["birthday"], r["sex"]))


# 函数功能：获取指定身份证号的相关信息（包括行政区域，生日，性别）
# 参数：
#   cardno str, 合法的身份证号
# 返回值：
#   字典类型，格式为：{"err": 0, "area": "湖北省武汉市江夏区", "birthday": "1990年8月13日", "sex": "男"}
#   如果err字段为0，表示获取信息成功，为1表示获取信息失败（原因可能是身份证号位数错误、含有非法字符、校验码错误、行政区域不存在）

def get_idcard_info(cardno):
    ret = {"err": 1, "area": "", "birthday": "", "sex": ""}

    # 初级校验
    cardno = cardno.upper()
    if re.fullmatch("[1-6]\\d{16}[\\d|X]", cardno) == None:
        return ret

    # 利用身份证号最末尾的校验码进一步校验
    code = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    i, s = 0, 0
    while i < 17:
        s += int(cardno[i]) * code[i]
        i += 1

    s = (12 - (s % 11)) % 11

    if s == 10:
        s = "X"
    else:
        s = str(s)

    if s != cardno[17]:
        return ret

    # 提取身份证号中的信息
    area_code = cardno[:6]
    with open("idcard_addr_code.txt", "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if line == "":
                break

            if line[:6] == area_code:
                ret["area"] = line.split()[1]
                break

    birthday = cardno[6:14]
    birthday = "%s年%d月%d日" % (birthday[0:4], int(birthday[4:6]), int(birthday[6:8]))
    ret["birthday"] = birthday

    sex = "男"
    if int(cardno[-2]) % 2 == 0:
        sex = "女"
    ret["sex"] = sex

    if ret["area"] != "" and ret["birthday"] != "" and ret["sex"] != "":
        ret["err"] = 0

    return ret


if __name__ == '__main__':
    main()
