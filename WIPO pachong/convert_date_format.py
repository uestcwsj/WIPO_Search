def convert_date_format(date_str):
    # 分割日期字符串
    parts = date_str.split('.')
    # 检查日期是否正确分割为三部分
    if len(parts) == 3:
        # 重新组合日期为 'YYYY.MM.DD' 格式
        new_date = f"{parts[2]}.{parts[1]}.{parts[0]}"
        return new_date
    else:
        # 如果日期格式不正确，返回错误信息
        return " "
