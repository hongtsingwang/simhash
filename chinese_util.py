#!/usr/bin/python
# -*- coding: utf-8 -*-


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


def is_normal(uchar):
    """判断是否非汉字，数字和英文字符"""
    if (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


def B2Q(uchar):
    """半角转全角"""
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
        return uchar
    if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return unichr(inside_code)


def Q2B(uchar):
    """全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
        return uchar
    return unichr(inside_code)


def stringQ2B(ustring):
    """把字符串全角转半角"""
    return "".join([Q2B(uchar) for uchar in ustring])


def uniform(ustring):
    """格式化字符串，完成全角转半角，大写转小写的工作"""
    return stringQ2B(ustring).lower()


def string2List(ustring):
    """将ustring按照中文，字母，数字分开"""
    retList = []
    utmp = []
    for uchar in ustring:
        if is_other(uchar):
            if len(utmp) == 0:
                continue
            else:
                retList.append("".join(utmp))
                utmp = []
        else:
            utmp.append(uchar)
    if len(utmp) != 0:
        retList.append("".join(utmp))
    return retList


def remove_uesless_char(ustring):
    """
    ustring: 输入字符串
    返回无中文，英文， 数字的字符串
    """
    result = ""
    for uchar in ustring:
        if is_other(uchar):
            result += " "
        else:
            result += uchar
    return result


def is_en_visible(uchar):
    if (uchar >= u'\u0021' and uchar <= u'\u007e'):
        return True
    else:
        return False


def is_en_biaodian(uchar):
    return is_en_visible(uchar) and not is_alphabet(uchar) and not is_number(uchar)


def replace_biaodian_to_space(ustring):
    uret = ""
    for i in range(len(ustring)):
        if is_en_biaodian(ustring[i]):
            uret += ' '
        else:
            uret += ustring[i]
    return uret


# 标点符号set
cn_biaodian_set = set([u'\u00b7', u'\u00d7', u'\u2014', u'\u2018', u'\u2019', u'\u201c', u'\u201d', u'\u2026', u'\u3001', u'\u3002', u'\u300a',
                       u'\u300b', u'\u300e', u'\u300f', u'\u3010', u'\u3011', u'\uff01', u'\uff08', u'\uff09', u'\uff0c', u'\uff1a', u'\uff1b', u'\uff1f'])
# 至少一个汉字，并且由汉字字母数字组成


def is_cn_sentences(ustr):
    has_cn = False
    for i in range(len(ustr)):
        if is_chinese(ustr[i]):
            has_cn = True
        if not (is_normal(ustr[i]) or ustr[i] in cn_biaodian_set or is_en_visible(ustr[i])):
            return False
    return has_cn


def sentences_cn_num(ustr):
    cn_num = 0
    for i in range(len(ustr)):
        if is_chinese(ustr[i]):
            cn_num += 1
    return cn_num


if __name__ == '__main__':
    print replace_biaodian_to_space("abc'def|ghi?aaa..,kad")
    s = "这是HAHA123..~~"
    print sentences_cn_num(s.decode("utf-8"))
