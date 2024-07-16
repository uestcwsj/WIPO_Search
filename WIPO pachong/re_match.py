import re
from lxml import etree

def re_match(source_text, match_text, combo_text=False):
    """
    :param source_text: 原始要解析的html字符串
    :param match_text: re表达式中要配对的值
    :param combo_text: 关键字参数 是否是作何参数
    :return:
    """
    obj = re.compile(
        r'<div class="ps-biblio-data".*?<div id="detailMainForm:MyTabViewId:.*?>%s(?P<val>.*?)<div id' % match_text,
        re.S)
    result = obj.finditer(source_text)
    data_list = []

    for item in result:
        html = item.group('val')
        #print(html)
        tree = etree.HTML(html)

        data_list = tree.xpath('//span//text()')

    if combo_text:

        result_list = [x.replace('\t', ' ').replace('\n' ' ').replace('  ', ' ') for x in data_list]

        count = 1
        comb_str = ''
        length = len(result_list)

        for item in result_list:
            if item == '':
                count += 1
                continue

            if count == length:
                comb_str += item
                break
            comb_str += item + '\n'
            count += 1
        return comb_str

    str_ = ' '.join(data_list)
    result_str = re.sub(r'\n|\t', '', str_.strip())
    return result_str