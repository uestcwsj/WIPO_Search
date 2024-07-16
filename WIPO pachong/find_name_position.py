def find_name_position(name_str, target_name):
    # 将传入的字符串分割成名字列表
    names_list = name_str.split()

    # 遍历名字列表，检查是否与目标名字匹配
    for index, name in enumerate(names_list):
        if name == target_name:
            return index + 1  # 返回名字的位置，索引从1开始计数

    # 如果没有找到名字，返回-1
    return -1
