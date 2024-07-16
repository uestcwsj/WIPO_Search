import re

def format_chinese_names(name_str):
    # 使用正则表达式匹配中文姓名和英文名
    # 匹配模式为中文姓名后跟空格和英文名，或者只有中文姓名
    pattern = r'([\u4e00-\u9fa5]+)(?:\s+([A-Z]\.\s*[A-Z]\.)+)?|([A-Z]\.\s*[A-Z]\.)'

    # 使用正则表达式找到所有匹配的姓名
    matches = re.findall(pattern, name_str)

    # 遍历所有匹配项，提取中文姓名
    chinese_names = []
    for match in matches:
        # 从匹配结果中选择中文姓名，如果有的话
        chinese_name = match[0] if match[0] else (match[2] if match[2] else '')
        if chinese_name:
            chinese_names.append(chinese_name)

    # 将列表中的中文姓名用' '连接成一个字符串，并去除可能的前后空格
    return ' '.join(chinese_names).strip()

