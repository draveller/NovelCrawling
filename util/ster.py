import re


def get_middle(text, start, end):
    """
    获取 start 和 end 之间的子串
    """
    if not end:
        return text.split(start)[-1]

    # 构建正则表达式，注意 re.DOTALL 用于匹配多行内容
    pattern = re.compile(f"{re.escape(start)}(.*?){re.escape(end)}", re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()  # 返回匹配的内容，并去除首尾空白
    return None  # 如果没有匹配到，返回 None
